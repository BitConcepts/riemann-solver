# Project Rules

## GPU Preference
Always prefer GPU computation over CPU when available, with automatic CPU fallback.
Set `RIEMANN_GPU_ENABLED=true` or call `set_config(gpu_enabled=True)` when CUDA
toolkit is installed. The `riemann.resources` module handles detection and fallback.

## Computation Safety
- Never use `multiprocessing.Pool` outside `if __name__ == '__main__'` guard
- Always use `get_config().max_workers` instead of `os.cpu_count()`
- Run `preflight.py` before any unattended computation
