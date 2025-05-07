import cv2
import numpy as np

from dct import dct2, dct_base, idct2


def main():
    image = load_image("test.png")

    q = input_value("Numero tra 1 e 100: ", 1, 100)
    meh = input_value(f"Numero tra 0 e {2*q - 2}: ", 0, 2 * q - 2)

    # np.set_printoptions(threshold=np.inf)

    print("Image: ")
    print(f"{image.shape}")
    print(image)

    D = dct_base(q)

    r, l = image.shape
    image = image - 128

    div = np.zeros((q, q))

    for i in range(q):
        for j in range(q):
            if (i + j) < 2 * meh - 2:
                div[i, j] = 1

    f = np.zeros((r, l))
    for i in range(0, r, q):
        for j in range(0, l, q):
            if i + q <= r and j + q <= l:
                f[i : i + q, j : j + q] = dct2(image[i : i + q, j : j + q], D)
                f[i : i + q, j : j + q] = np.multiply(f[i : i + q, j : j + q], div)

    for i in range(0, r, q):
        for j in range(0, l, q):
            if i + q <= r and j + q <= l:
                f[i : i + q, j : j + q] = idct2(f[i : i + q, j : j + q], D)

    f = f + 128

    print("Risultato: ")
    print(f"{f.shape}")
    print(np.round(f, 2))

    cv2.imwrite("result.jpg", f)


def load_image(image_path):
    """
    Carica un'immagine in scala di grigi.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Impossibile caricare l'immagine da {image_path}")
    return image


def input_value(msg, min, max):
    while True:
        try:
            x = int(input(msg))
            if x >= min and x <= max:
                return x
        except:
            pass
        print(f"Inserisci un numero intero tra {min} e {max}.")


if __name__ == "__main__":
    main()

# Codice per la matrice di quantizzazione

# if(q<=50):
#     q=(100-q)/50
# else:
#     q= 50/q

#      # puoi cambiarlo per regolare la compressione
# Q = np.array([  # Matrice di quantizzazione JPEG standard 8x8
#     [16,11,10,16,24,40,51,61],
#     [12,12,14,19,26,58,60,55],
#     [14,13,16,24,40,57,69,56],
#     [14,17,22,29,51,87,80,62],
#     [18,22,37,56,68,109,103,77],
#     [24,35,55,64,81,104,113,92],
#     [49,64,78,87,103,121,120,101],
#     [72,92,95,98,112,100,103,99]
# ])
# Qq = Q * q
# div=np.zeros((8,8))
# for i in range(0,8):
#     for j in range(0,8):
#         div= 1/(max(1,Qq[i,j]))
