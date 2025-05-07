import numpy as np

from dct import dct2, dct_base, idct2


def main():
    ex0 = np.array(range(0, 64)) * 0 + 10
    ex1 = np.array(range(0, 64))
    ex2 = np.tensordot(ex0, ex1, axes=0)

    D = dct_base(ex2)

    c = dct2(ex2, D)
    print(c)

    f = idct2(c, D)
    print(abs(f.round(2)))


if __name__ == "__main__":
    main()
