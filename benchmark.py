import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import dct, idct

from dct import dct2 as custom_dct2
from dct import dct_base as custom_dct_base
from dct import idct2 as custom_idct2


def main():
    def dct2(a):
        return dct(dct(a.T, norm="ortho").T, norm="ortho")

    def idct2(a):
        return idct(idct(a.T, norm="ortho").T, norm="ortho")

    # Diverse dimensioni da testare
    sizes = [32, 64, 128, 256, 512, 1024]
    times = []
    times_c = []

    for size in sizes:
        # Genera una matrice random di dimensione NxN
        matrix = np.random.rand(size, size)

        start = time.perf_counter()

        # DCT2
        transformed = dct2(matrix)

        # "Compressione": azzera le alte frequenze
        cutoff = size // 4
        transformed[cutoff:, cutoff:] = 0

        # IDCT2
        reconstructed = idct2(transformed)

        end = time.perf_counter()
        elapsed_time = end - start
        times.append(elapsed_time)

        start = time.perf_counter()

        D = custom_dct_base(size)
        transformed_c = custom_dct2(matrix, D)
        reconstructed = custom_idct2(transformed, D)
        end = time.perf_counter()
        elapsed_time = end - start
        times_c.append(elapsed_time)

    sizes_np = np.array(sizes, dtype=np.float64)
    nlogn = sizes_np**2 * np.log2(sizes_np)  # perché fai DCT2 su matrice NxN
    n3 = sizes_np**3

    norm_factor = times[0] / nlogn[0]
    nlogn_curve = norm_factor * nlogn

    norm_factor3 = times[0] / n3[0]
    n3_curve = norm_factor3 * n3

    # Grafico semilogaritmico
    plt.figure(figsize=(8, 6))
    plt.semilogy(
        sizes, nlogn_curve, marker="o", linestyle="-", color="green", label="O(n^2)"
    )
    plt.semilogy(
        sizes, n3_curve, marker="o", linestyle="-", color="black", label="O(n^3)"
    )
    plt.semilogy(
        sizes,
        times,
        marker="o",
        linestyle="-",
        color="blue",
        label="DCT2 + IDCT2 (scipy)",
    )
    plt.semilogy(
        sizes,
        times_c,
        marker="o",
        linestyle="-",
        color="red",
        label="DCT2 + IDCT2 (custom)",
    )
    plt.xlabel("Dimensione matrice (NxN)")
    plt.ylabel("Tempo di compressione (s) [Scala logaritmica]")
    plt.title("Tempi di compressione DCT2 + IDCT2 custom vs scipy")
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig("benchmark.jpeg", format="jpeg")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
