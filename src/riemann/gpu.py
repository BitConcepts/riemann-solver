"""GPU-accelerated matrix operations for Galerkin and spectral computations.

Provides transparent GPU acceleration via CuPy (CUDA) or PyTorch when
available, with automatic fallback to NumPy/SciPy on CPU.

The CvS Galerkin matrix at large N (N=100..250) and high dps is the
primary bottleneck. The archimedean integral dominates wall-clock time.
GPU acceleration targets:
  1. Matrix assembly (parallel element computation)
  2. Symmetric eigendecomposition (cuSOLVER / torch.linalg.eigh)
  3. Eigenvector Fourier analysis (zero extraction)

Note: Arbitrary-precision (mpmath) operations cannot run on GPU.
The strategy is: build the matrix in mpmath, convert to float64/float128
for the eigendecomposition on GPU, then refine in mpmath.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

import numpy as np


class Backend(Enum):
    """Available compute backends."""

    NUMPY = "numpy"
    CUPY = "cupy"
    TORCH_CUDA = "torch_cuda"
    TORCH_MPS = "torch_mps"  # Apple Silicon


def detect_backend() -> Backend:
    """Detect the best available GPU backend."""
    # Try CuPy (NVIDIA CUDA)
    try:
        import cupy as cp

        cp.cuda.runtime.getDeviceCount()
        return Backend.CUPY
    except Exception:
        pass

    # Try PyTorch CUDA
    try:
        import torch

        if torch.cuda.is_available():
            return Backend.TORCH_CUDA
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return Backend.TORCH_MPS
    except ImportError:
        pass

    return Backend.NUMPY


def get_backend_info() -> dict:
    """Return information about the active compute backend."""
    backend = detect_backend()
    info = {"backend": backend.value, "gpu_available": backend != Backend.NUMPY}

    if backend == Backend.CUPY:
        import cupy as cp

        dev = cp.cuda.Device()
        info["device_name"] = dev.attributes.get("DeviceName", "unknown")
        info["memory_total"] = dev.mem_info[1]
    elif backend in (Backend.TORCH_CUDA, Backend.TORCH_MPS):
        import torch

        if backend == Backend.TORCH_CUDA:
            info["device_name"] = torch.cuda.get_device_name(0)
            info["memory_total"] = torch.cuda.get_device_properties(0).total_mem
        else:
            info["device_name"] = "Apple MPS"

    return info


def symmetric_eigh(matrix: np.ndarray, backend: Backend | None = None) -> tuple[np.ndarray, np.ndarray]:
    """GPU-accelerated symmetric eigendecomposition.

    Args:
        matrix: Real symmetric matrix as numpy array
        backend: Force a specific backend (auto-detect if None)

    Returns:
        (eigenvalues, eigenvectors) sorted by eigenvalue
    """
    if backend is None:
        backend = detect_backend()

    if backend == Backend.CUPY:
        import cupy as cp
        from cupyx.scipy.linalg import eigh as cp_eigh

        gpu_mat = cp.asarray(matrix)
        eigenvalues, eigenvectors = cp_eigh(gpu_mat)
        return cp.asnumpy(eigenvalues), cp.asnumpy(eigenvectors)

    elif backend in (Backend.TORCH_CUDA, Backend.TORCH_MPS):
        import torch

        device = "cuda" if backend == Backend.TORCH_CUDA else "mps"
        t_mat = torch.from_numpy(matrix).to(device=device, dtype=torch.float64)
        eigenvalues, eigenvectors = torch.linalg.eigh(t_mat)
        return eigenvalues.cpu().numpy(), eigenvectors.cpu().numpy()

    else:
        from scipy.linalg import eigh

        return eigh(matrix)


def parallel_matrix_build(
    func: Any,
    dim: int,
    backend: Backend | None = None,
) -> np.ndarray:
    """Build a symmetric matrix in parallel using GPU kernels.

    Args:
        func: Callable(i, j) -> float for matrix elements
        dim: Matrix dimension
        backend: Force a specific backend

    Returns:
        dim x dim numpy array
    """
    if backend is None:
        backend = detect_backend()

    # For now, all backends use numpy construction
    # GPU kernels for arbitrary element functions would require JIT compilation
    matrix = np.zeros((dim, dim), dtype=np.float64)
    for i in range(dim):
        for j in range(i, dim):
            val = func(i, j)
            matrix[i, j] = val
            matrix[j, i] = val
    return matrix


def mpf_matrix_to_float64(mp_matrix: Any) -> np.ndarray:
    """Convert an mpmath matrix to float64 numpy array.

    This is the bridge between arbitrary-precision assembly and
    GPU-accelerated eigendecomposition.

    Warning: precision loss occurs. Use this for initial eigenvalue
    estimates, then refine in mpmath.
    """
    rows, cols = mp_matrix.rows, mp_matrix.cols
    result = np.zeros((rows, cols), dtype=np.float64)
    for i in range(rows):
        for j in range(cols):
            result[i, j] = float(mp_matrix[i, j])
    return result


if __name__ == "__main__":
    info = get_backend_info()
    print("GPU Backend Detection:")
    for k, v in info.items():
        print(f"  {k}: {v}")
