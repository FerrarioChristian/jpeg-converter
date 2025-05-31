import os

import cv2
import numpy as np
from PIL import Image

from .dct import dct2, dct_base, idct2


def compress(image_path, f, d, output_path="./results/result.bmp"):
    image = load_image(image_path).astype(np.float32)

    check_parameters(f, d, min(image.shape))

    print_state("Original image: ", image)

    D = dct_base(f)

    image = cut_image(image, f)
    image = apply_dct(image, f, D)
    image = cut_frequencies(image, f, d)

    print_state("Image after DCT: ", image)

    image = apply_idct(image, f, D)

    print_state("Image after IDCT: ", image)

    image = np.clip(image, 0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)
    print("Image saved at ", output_path)


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
    image = Image.open(image_path).convert("L")  # Converti in scala di grigi
    if image is None:
        raise ValueError(f"Fail to load image from {image_path}")
    return np.array(image)


def input_value(msg, min, max):
    while True:
        try:
            x = int(input(msg))
            if x >= min and x <= max:
                return x
        except:
            pass
        print(f"The value must be an integer between {min} and {max}")


def print_state(msg, matrix):
    """
    Stampa lo stato della matrice.
    """
    print(msg)
    print(f"{matrix.shape}")
    print(matrix)


def check_parameters(f, d, max_f):
    """
    Controlla i parametri f e d.
    """
    if f < 1 or f > max_f:
        raise ValueError(
            f"The value of F must be greater than 0 and less than or equal to {max_f}"
        )
    if d < 0 or d > 2 * f - 2:
        raise ValueError(f"The value of D must be between 0 and {2 * f - 2}")
