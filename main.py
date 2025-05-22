# from sys import maxsize as sys_maxsize

import cv2
import numpy as np

from dct import dct2, dct_base, idct2


def main():
    image = load_image("./images/test.bmp").astype(np.float32)

    f = input_value(f"Numero tra 1 e {min(image.shape)}: ", 1, min(image.shape))
    d = input_value(f"Numero tra 0 e {2*f - 2}: ", 0, 2 * f - 2)

    # np.set_printoptions(threshold=sys_maxsize)

    print_state("Immagine originale: ", image)

    D = dct_base(f)

    image = cut_image(image, f)
    image = apply_dct(image, f, D)
    image = cut_frequencies(image, f, d)

    print_state("Immagine dopo DCT: ", image)

    image = apply_idct(image, f, D)

    print_state("Immagine dopo IDCT: ", image)

    image = np.clip(image, 0, 255).astype(np.uint8)
    cv2.imwrite("result.bmp", image)


def apply_dct(image, f, D):
    """
    Applica la DCT a blocchi di dimensione f x f dell'immagine.
    """
    r, l = image.shape
    image = image - 128

    for i in range(0, r, f):
        for j in range(0, l, f):
            if i + f <= r and j + f <= l:
                image[i : i + f, j : j + f] = dct2(image[i : i + f, j : j + f], D)

    return image


def apply_idct(image, f, D):
    """
    Applica la IDCT a blocchi di dimensione f x f dell'immagine.
    """
    r, l = image.shape

    for i in range(0, r, f):
        for j in range(0, l, f):
            if i + f <= r and j + f <= l:
                image[i : i + f, j : j + f] = idct2(image[i : i + f, j : j + f], D)

    image = image + 128

    return image


def cut_frequencies(image, f, d):
    div = np.zeros((f, f))
    for i in range(f):
        for j in range(f):
            if (i + j) < d:
                div[i, j] = 1

    for i in range(0, image.shape[0], f):
        for j in range(0, image.shape[1], f):
            if i + f <= image.shape[0] and j + f <= image.shape[1]:
                image[i : i + f, j : j + f] = np.multiply(
                    image[i : i + f, j : j + f], div
                )
    return image


def cut_image(image, f):
    """
    Taglia l'immagine in modo che le dimensioni siano multipli di f.
    """
    r, l = image.shape
    r = r - (r % f)
    l = l - (l % f)
    image = image[0:r, 0:l]

    return image


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


def print_state(msg, matrix):
    """
    Stampa lo stato della matrice.
    """
    print(msg)
    print(f"{matrix.shape}")
    print(matrix)


if __name__ == "__main__":
    main()

# Codice per la matrice di quantizzazione

# if(q<=50):
#     q=(100-q)/50
# else:
#     q= 50/q
# Q = np.array([
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
