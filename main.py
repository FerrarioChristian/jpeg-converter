import numpy as np

from dct import dct2, dct_base, idct2


def main():
    ex0 = np.array(range(0, 64)) * 0 + 10
    ex1 = np.array(range(0, 64))
    ex2 = np.tensordot(ex0, ex1, axes=0)
    print("ex2")
    print(ex2.shape)
    print(ex2)
    D = dct_base()
    
    r, l = ex2.shape


    f = np.zeros((r, l))
    for i in range(0, r, 8):
        for j in range(0, l, 8):
            submatrix = ex2[i:i+8, j:j+8]
            f[i:i+8, j:j+8]= dct2(submatrix, D)

   
    for i in range(0, r, 8):
        for j in range(0, l, 8):
            submatrixC = f[i:i+8, j:j+8]
            f[i:i+8, j:j+8]= idct2(submatrixC, D)
        
    print("f")
    print(f.shape)
    print(np.round(f, 2))
    

    
        
if __name__ == "__main__":
    main()
