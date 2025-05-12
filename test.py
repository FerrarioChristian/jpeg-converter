import numpy as np

import dct

test1 = [231, 32, 233, 161, 24, 71, 140, 245]

base = dct.dct_base(test1.__len__())
dct1 = dct.dct(test1, base)
print("DCT: ", end="")
for i in range(len(test1)):
    print(f"{dct1[i]:.2e}", end=", ")
idct1 = dct.idct(dct1, base)
print("\nIDCT: ", idct1)


test2 = [
    [231, 32, 233, 161, 24, 71, 140, 245],
    [247, 40, 248, 245, 124, 204, 36, 107],
    [234, 202, 245, 167, 9, 217, 239, 173],
    [193, 190, 100, 167, 43, 180, 8, 70],
    [11, 24, 210, 177, 81, 243, 8, 112],
    [97, 195, 203, 47, 125, 114, 165, 181],
    [193, 70, 174, 167, 41, 30, 127, 245],
    [87, 149, 57, 192, 65, 129, 178, 228],
]
base2 = dct.dct_base(test2.__len__())
dct2 = dct.dct2(test2, base2)
print("\nDCT2: ", end="")
np.set_printoptions(precision=2)
print(dct2)
idct2 = dct.idct2(dct2, base2)
print("IDCT2: ", idct2)
