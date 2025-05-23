# from sys import maxsize as sys_maxsize

import os

import cv2
import numpy as np

from dct import dct2, dct_base, idct2


def load_image(image_path):
    """
    Carica un'immagine in scala di grigi.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Impossibile caricare l'immagine da {image_path}")
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


def backend_func(imageUrl, f, d):
    image = load_image(imageUrl).astype(np.float32)

    print("Image: ")
    print(f"{image.shape}")
    print(image)

    D = dct_base(f)

    image = cut_image(image, f)

    r, l = image.shape
    image = image - 128

    div = np.zeros((f, f))

    for i in range(f):
        for j in range(f):
            if (i + j) < 2 * d - 2:
                div[i, j] = 1

    for i in range(0, r, f):
        for j in range(0, l, f):
            if i + f <= r and j + f <= l:
                image[i : i + f, j : j + f] = dct2(image[i : i + f, j : j + f], D)
                image[i : i + f, j : j + f] = np.multiply(
                    image[i : i + f, j : j + f], div
                )

    for i in range(0, r, f):
        for j in range(0, l, f):
            if i + f <= r and j + f <= l:
                image[i : i + f, j : j + f] = idct2(image[i : i + f, j : j + f], D)

    image = image + 128

    print("Risultato: ")
    print(f"{image.shape}")
    print(np.round(image, 2))

    image = np.clip(image, 0, 255).astype(np.uint8)
    os.makedirs("./results", exist_ok=True)
    cv2.imwrite("./results/result.bmp", image)
