import numpy as np


from dct import dct2, dct_base, idct2
import cv2

# Carica direttamente in scala di grigi
gray_matrix = cv2.imread("./test.png", cv2.IMREAD_GRAYSCALE)
def main():
    ex0 = np.array(range(0, 64)) * 0 + 10
    ex1 = np.array(range(0, 64))
    ex2 = gray_matrix
    print("ex2")
    print(ex2.shape)
    print(ex2)
    D = dct_base()
    
    r, l = ex2.shape
    ex2=ex2-128

    print("passa sta q")
    q = int(input("Inserisci un numero intero compreso tra 1 e 100 "))
    if(q<1 or q>100):
        q = int(input("Inserisci un numero intero compreso tra 1 e 100 "))
    if(q<=50):
        q=(100-q)/50
    else:
        q= 50/q
        
         # puoi cambiarlo per regolare la compressione
    Q = np.array([  # Matrice di quantizzazione JPEG standard 8x8
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])
    Qq = Q * q
    div=np.zeros((8,8))
    for i in range(0,8):
        for j in range(0,8):
            div= 1/(max(1,Qq[i,j]))

    f = np.zeros((r, l))
    for i in range(0, r, 8):
        for j in range(0, l, 8):
            submatrix = ex2[i:i+8, j:j+8]
            f[i:i+8, j:j+8]= dct2(submatrix, D)
            np.multiply(f[i:i+8, j:j+8], div)
    

    
    for i in range(0, r, 8):
        for j in range(0, l, 8):
            submatrixC = f[i:i+8, j:j+8]
            f[i:i+8, j:j+8]= idct2(submatrixC, D)
    
    f=f+128
    print("f")
    print(f.shape)
    print(np.round(f, 2))
    
    cv2.imwrite('immagine_salvata.jpg', gray_matrix)

    
        
if __name__ == "__main__":
    main()
