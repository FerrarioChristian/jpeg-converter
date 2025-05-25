import os
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import dct, idct

from converter import dct2 as custom_dct2
from converter import dct_base as custom_dct_base
from converter import idct2 as custom_idct2


def scipy_dct2(a):
    return dct(dct(a.T, norm="ortho").T, norm="ortho")


def scipy_idct2(a):
    return idct(idct(a.T, norm="ortho").T, norm="ortho")


def plot_benchmarks(sizes, times_scipy, times_custom):
    """Crea e salva un grafico semilogaritmico dei tempi di benchmark."""
    sizes_np = np.array(sizes, dtype=np.float64)
    nlogn = sizes_np**2 * np.log2(sizes_np)
    n3 = sizes_np**3

    norm_factor_nlogn = times_scipy[0] / nlogn[0] if nlogn[0] != 0 else 1
    nlogn_curve = norm_factor_nlogn * nlogn

    norm_factor_n3 = times_custom[0] / n3[0] if n3[0] != 0 else 1
    n3_curve = norm_factor_n3 * n3

    plt.figure(figsize=(10, 7))
    plt.semilogy(
        sizes,
        nlogn_curve,
        marker="o",
        linestyle="-",
        color="green",
        label="O(N^2 log N)",
    )
    plt.semilogy(
        sizes, n3_curve, marker="o", linestyle="-", color="black", label="O(N^3)"
    )
    plt.semilogy(
        sizes,
        times_scipy,
        marker="o",
        linestyle="-",
        color="blue",
        label="DCT2 + IDCT2 (scipy)",
    )
    plt.semilogy(
        sizes,
        times_custom,
        marker="o",
        linestyle="-",
        color="red",
        label="DCT2 + IDCT2 (custom)",
    )
    plt.xlabel("Dimensione matrice (NxN)")
    plt.ylabel("Tempo di esecuzione (s) [Scala logaritmica]")
    plt.title("Tempi di esecuzione DCT2 + IDCT2: custom vs scipy")
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)

    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, "benchmark.jpeg")
    plt.savefig(filepath, format="jpeg")
    plt.tight_layout()
    plt.show()


def benchmark_dct(sizes):
    """Misura i tempi di esecuzione per la DCT2 e IDCT2 (scipy e custom) per diverse dimensioni."""
    times_scipy = []
    times_custom = []

    for size in sizes:
        matrix = np.random.rand(size, size)

        # Benchmark scipy DCT2 + IDCT2
        start_scipy = time.perf_counter()
        transformed_scipy = scipy_dct2(matrix)
        cutoff = size // 4
        transformed_scipy[cutoff:, cutoff:] = 0
        scipy_idct2(transformed_scipy)
        end_scipy = time.perf_counter()
        times_scipy.append(end_scipy - start_scipy)

        # Benchmark custom DCT2 + IDCT2
        start_custom = time.perf_counter()
        D = custom_dct_base(size)
        transformed_custom = custom_dct2(matrix, D)
        transformed_custom[cutoff:, cutoff:] = 0
        custom_idct2(transformed_custom, D)
        end_custom = time.perf_counter()
        times_custom.append(end_custom - start_custom)

    return times_scipy, times_custom


def main():
    sizes_to_test = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
    times_scipy, times_custom = benchmark_dct(sizes_to_test)
    plot_benchmarks(sizes_to_test, times_scipy, times_custom)


if __name__ == "__main__":
    main()
