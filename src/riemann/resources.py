"""Resource safety — configurable CPU/RAM/GPU limits to prevent lockups.

All compute modules import limits from here. Defaults are conservative.

Configuration priority (highest first):
  1. Function call: set_config(max_cpus=8, gpu_enabled=True)
  2. Environment variables: RIEMANN_MAX_CPUS=8, RIEMANN_GPU_ENABLED=true
  3. Config file: riemann.resources.toml in project root
  4. Built-in defaults (75% CPU, 70% RAM, GPU off)

ROOT CAUSE OF PREVIOUS LOCKUP:
  multiprocessing.Pool(os.cpu_count()) without __name__ guard on Windows
  causes recursive fork bomb. NEVER call Pool outside __name__ == '__main__'.

RULES:
  1. NEVER call multiprocessing.Pool outside `if __name__ == '__main__'`
  2. ALWAYS use get_config().max_workers instead of os.cpu_count()
  3. ALWAYS call check_resources() before heavy computation
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ResourceConfig:
    """Centralized resource configuration.

    Defaults tuned for i9-14900F (32 cores), 64GB RAM, RTX 4070 SUPER.
    """

    # CPU — default: use 75% of cores minus 4 reserved for OS
    cpu_fraction: float = 0.75
    max_cpus: Optional[int] = None
    reserved_cpus: int = 4

    # RAM — default: use 70% of total, keep 4GB free minimum
    ram_fraction: float = 0.70
    max_ram_gb: Optional[float] = None
    min_free_ram_gb: float = 4.0

    # GPU — default: OFF (cuSOLVER needs full CUDA Toolkit)
    gpu_enabled: bool = False
    gpu_device: int = 0
    gpu_max_vram_gb: Optional[float] = None

    # Per-worker memory estimate (MB)
    worker_memory_mb: int = 250

    @property
    def total_cpus(self) -> int:
        return os.cpu_count() or 1

    @property
    def max_workers(self) -> int:
        """Maximum safe worker count respecting CPU + RAM limits."""
        # CPU limit
        from_fraction = max(1, int(self.total_cpus * self.cpu_fraction) - self.reserved_cpus)
        if self.max_cpus is not None:
            from_fraction = min(from_fraction, self.max_cpus)

        # RAM limit
        headroom = self.available_ram_gb - self.min_free_ram_gb
        from_memory = max(1, int(headroom * 1024 / self.worker_memory_mb))

        return max(1, min(from_fraction, from_memory))

    @property
    def total_ram_gb(self) -> float:
        try:
            import psutil
            return psutil.virtual_memory().total / (1024 ** 3)
        except ImportError:
            return 64.0

    @property
    def free_ram_gb(self) -> float:
        try:
            import psutil
            return psutil.virtual_memory().available / (1024 ** 3)
        except ImportError:
            return 32.0

    @property
    def available_ram_gb(self) -> float:
        budget = self.total_ram_gb * self.ram_fraction
        if self.max_ram_gb is not None:
            budget = min(budget, self.max_ram_gb)
        return min(self.free_ram_gb, budget)

    @property
    def gpu_available(self) -> bool:
        if not self.gpu_enabled:
            return False
        try:
            import cupy as cp
            cp.cuda.Device(self.gpu_device).use()
            return True
        except Exception:
            return False

    @property
    def gpu_vram_gb(self) -> Optional[float]:
        if not self.gpu_available:
            return None
        try:
            import cupy as cp
            free, total = cp.cuda.Device(self.gpu_device).mem_info
            vram = free / (1024 ** 3)
            if self.gpu_max_vram_gb is not None:
                vram = min(vram, self.gpu_max_vram_gb)
            return vram
        except Exception:
            return None


# ── Singleton ────────────────────────────────────────────────────────

_config: Optional[ResourceConfig] = None


def get_config() -> ResourceConfig:
    """Get the singleton config, loading from env/file on first call."""
    global _config
    if _config is None:
        _config = _load_config()
    return _config


def set_config(**kwargs) -> ResourceConfig:
    """Override config fields.

    Example:
        set_config(max_cpus=8, gpu_enabled=True, max_ram_gb=32)
    """
    global _config
    cfg = get_config()
    for key, val in kwargs.items():
        if val is not None and hasattr(cfg, key):
            setattr(cfg, key, val)
    _config = cfg
    return cfg


def _load_config() -> ResourceConfig:
    """Load from env vars → config file → defaults."""
    cfg = ResourceConfig()
    _ENV = {
        "RIEMANN_CPU_FRACTION": ("cpu_fraction", float),
        "RIEMANN_MAX_CPUS": ("max_cpus", int),
        "RIEMANN_RESERVED_CPUS": ("reserved_cpus", int),
        "RIEMANN_RAM_FRACTION": ("ram_fraction", float),
        "RIEMANN_MAX_RAM_GB": ("max_ram_gb", float),
        "RIEMANN_MIN_FREE_RAM_GB": ("min_free_ram_gb", float),
        "RIEMANN_GPU_ENABLED": ("gpu_enabled", lambda x: x.lower() in ("1", "true", "yes")),
        "RIEMANN_GPU_DEVICE": ("gpu_device", int),
        "RIEMANN_GPU_MAX_VRAM_GB": ("gpu_max_vram_gb", float),
        "RIEMANN_WORKER_MEMORY_MB": ("worker_memory_mb", int),
    }
    for env_key, (attr, conv) in _ENV.items():
        val = os.environ.get(env_key)
        if val is not None:
            try:
                setattr(cfg, attr, conv(val))
            except (ValueError, TypeError):
                pass

    # Config file
    for p in [Path("riemann.resources.toml"), Path.home() / ".riemann" / "resources.toml"]:
        if p.exists():
            try:
                import tomllib
                with open(p, "rb") as f:
                    data = tomllib.load(f)
                for key, val in data.items():
                    if hasattr(cfg, key) and os.environ.get(f"RIEMANN_{key.upper()}") is None:
                        setattr(cfg, key, val)
            except Exception:
                pass
            break

    return cfg


def check_resources(label: str = "computation") -> bool:
    """Pre-flight check. Returns False and prints warning if unsafe."""
    cfg = get_config()
    if cfg.free_ram_gb < cfg.min_free_ram_gb:
        print(f"  ⚠ {cfg.free_ram_gb:.1f}GB RAM free < {cfg.min_free_ram_gb}GB min. "
              f"Skipping {label}.")
        return False
    return True


def print_summary():
    """Print resource summary."""
    cfg = get_config()
    print(f"  CPU: {cfg.total_cpus} total × {cfg.cpu_fraction:.0%} "
          f"- {cfg.reserved_cpus} reserved = {cfg.max_workers} workers")
    if cfg.max_cpus:
        print(f"       (hard cap: {cfg.max_cpus})")
    print(f"  RAM: {cfg.total_ram_gb:.1f}GB total × {cfg.ram_fraction:.0%} "
          f"= {cfg.available_ram_gb:.1f}GB budget ({cfg.free_ram_gb:.1f}GB free)")
    if cfg.gpu_enabled:
        vram = cfg.gpu_vram_gb
        if vram is not None:
            print(f"  GPU: enabled, device {cfg.gpu_device}, {vram:.1f}GB VRAM")
        else:
            print(f"  GPU: enabled but not available (install CUDA Toolkit)")
    else:
        print(f"  GPU: disabled (set gpu_enabled=True or RIEMANN_GPU_ENABLED=true)")


if __name__ == "__main__":
    print("Resource Configuration:")
    print_summary()
    print(f"\n  Override via env vars or set_config():")
    print(f"    RIEMANN_MAX_CPUS=8  RIEMANN_GPU_ENABLED=true  RIEMANN_MAX_RAM_GB=32")
    print(f"  Or create riemann.resources.toml / ~/.riemann/resources.toml")
