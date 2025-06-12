import os

import cv2
import numpy as np
from PIL import Image

from .dct import dct2, dct_base, idct2


import math
from .huffman import calculate_huffman_size

def compress(image_path, f, d, output_path="./results/result.bmp", use_huffman=True):
    image = load_image(image_path).astype(np.float32)

    check_parameters(f, d, min(image.shape))

    print_state("Original image: ", image)

    D = dct_base(f)

    image = cut_image(image, f)
    original_cut = np.copy(image)
    
    image = apply_dct(image, f, D)
    image = cut_frequencies(image, f, d)

    print_state("Image after DCT: ", image)
    
    # Estimate size based on Huffman encoding of DCT coefficients
    huffman_bytes = None
    if use_huffman:
        huffman_bytes = calculate_huffman_size(image)

    image = apply_idct(image, f, D)

    print_state("Image after IDCT: ", image)

    image = np.clip(image, 0, 255).astype(np.uint8)
    original_cut_uint8 = np.clip(original_cut, 0, 255).astype(np.uint8)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)
    
    # Calculate MSE and PSNR
    mse = np.mean((original_cut_uint8.astype(np.float32) - image.astype(np.float32)) ** 2)
    psnr = 100.0 # max if MSE is 0
    if mse > 0:
        psnr = 10 * math.log10((255.0 ** 2) / mse)
        
    # Generate Error Map (Difference Heatmap)
    diff = cv2.absdiff(original_cut_uint8, image)
    diff_enhanced = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
    error_map = cv2.applyColorMap(diff_enhanced, cv2.COLORMAP_JET)
    
    error_map_path = os.path.join(os.path.dirname(output_path), "error_map.bmp")
    cv2.imwrite(error_map_path, error_map)
    
    print("Image saved at ", output_path)
    
    return {
        "mse": mse,
        "psnr": psnr,
        "huffman_bytes": huffman_bytes,
        "output_path": output_path,
        "error_map_path": error_map_path
    }


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
