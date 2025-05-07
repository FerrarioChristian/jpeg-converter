import numpy as np


def dct_base(f):
    n = f.shape[0]
    D = np.zeros((n, n))
    alpha = alphas(n)

    for i in range(n):
        for j in range(n):
            D[i, j] = alpha[i] * np.cos((i * np.pi * (2 * j + 1) / (2 * n)))
    return D


def dct(f, D):
    return np.dot(D, f)


def idct(c, D):
    return np.dot(D.T, c)


def dct2(f, D):
    return D @ f @ D.T


def idct2(c, D):
    return D.T @ c @ D


def alphas(n):
    alpha = np.zeros(n)
    alpha[0] = 1 / np.sqrt(n)
    for i in range(1, n):
        alpha[i] = np.sqrt(2 / n)
    return alpha
