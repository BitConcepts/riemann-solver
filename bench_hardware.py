"""Benchmark this machine's hardware for Riemann solver workloads."""
import os
import time
import multiprocessing
import numpy as np

print("=" * 60)
print("  HARDWARE BENCHMARK FOR RIEMANN SOLVER")
print("=" * 60)

print(f"\nCPU cores (logical): {os.cpu_count()}")
print(f"Usable workers: {multiprocessing.cpu_count()}")

# GPU check
try:
    import cupy as cp
    print(f"CuPy: {cp.__version__}")
    props = cp.cuda.runtime.getDeviceProperties(0)
    gpu_name = props["name"].decode()
    dev = cp.cuda.Device(0)
    free, total = dev.mem_info
    print(f"GPU: {gpu_name}")
    print(f"VRAM: {total / 1024**3:.1f} GB total, {free / 1024**3:.1f} GB free")
    has_gpu = True
except Exception as e:
    print(f"GPU: not available ({e})")
    has_gpu = False

# Eigendecomposition benchmark
for n in [201, 501]:
    A = np.random.randn(n, n)
    A = (A + A.T) / 2

    t0 = time.time()
    np.linalg.eigh(A)
    t_cpu = time.time() - t0
    print(f"\n{n}x{n} symmetric eigh:")
    print(f"  CPU (numpy): {t_cpu * 1000:.1f}ms")

    if has_gpu:
        try:
            import cupy as cp
            A_gpu = cp.asarray(A)
            cp.cuda.Stream.null.synchronize()
            cp.linalg.eigh(A_gpu)
            cp.cuda.Stream.null.synchronize()
            t0 = time.time()
            cp.linalg.eigh(A_gpu)
            cp.cuda.Stream.null.synchronize()
            t_gpu = time.time() - t0
            print(f"  GPU (cupy):  {t_gpu * 1000:.1f}ms")
            print(f"  Speedup: {t_cpu / t_gpu:.1f}x")
        except Exception as e:
            print(f"  GPU eigh: unavailable ({type(e).__name__}: {e})")
            print(f"  (Install full CUDA Toolkit for cuSOLVER support)")

# Multiprocessing benchmark (digamma throughput)
import mpmath as mp
mp.mp.dps = 150

def digamma_batch(args):
    """Compute digamma for a batch of points."""
    count = 0
    for t_val in args:
        s = mp.mpc(0.25, t_val)
        mp.digamma(s)
        count += 1
    return count

t_values = [float(i) for i in range(200)]

# Single-core
t0 = time.time()
digamma_batch(t_values)
t_single = time.time() - t0
print(f"\n200 digamma evals at 150 dps:")
print(f"  Single-core: {t_single * 1000:.0f}ms ({t_single / 200 * 1000:.2f}ms/eval)")

# Multi-core
n_workers = min(os.cpu_count(), 16)
chunks = [t_values[i::n_workers] for i in range(n_workers)]
t0 = time.time()
with multiprocessing.Pool(n_workers) as pool:
    pool.map(digamma_batch, chunks)
t_multi = time.time() - t0
print(f"  {n_workers}-core: {t_multi * 1000:.0f}ms ({t_multi / 200 * 1000:.2f}ms/eval)")
print(f"  Speedup: {t_single / t_multi:.1f}x")

# Projection for CvS
elements_n50 = 101 * 101  # N=50 -> 101x101 matrix
elements_n100 = 201 * 201
single_rate = 200 / t_single  # evals per second
multi_rate = 200 / t_multi

print(f"\nProjected CvS matrix build times (estimated):")
print(f"  N=50  (101x101={elements_n50} elements):")
print(f"    Single-core: ~{elements_n50 / single_rate:.0f}s")
print(f"    {n_workers}-core: ~{elements_n50 / multi_rate:.0f}s")
print(f"  N=100 (201x201={elements_n100} elements):")
print(f"    Single-core: ~{elements_n100 / single_rate:.0f}s")
print(f"    {n_workers}-core: ~{elements_n100 / multi_rate:.0f}s")
