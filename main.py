# from sys import maxsize as sys_maxsize

import os

from cli import parse_arguments
from converter.backend import compress
from gui.gui import launch_gui

args = parse_arguments()
f = args.f
d = args.d
image_path = args.input


def main():
    """
    Main function to handle the compression process.
    It checks if the necessary parameters are provided. If not, it launches the GUI.
    If the parameters are valid, it calls the compress function to process the image.
    Parameters:
        f (int): The size of the blocks for DCT.
        d (int): The number of frequencies to keep.
        image_path (str): The path to the image file to be compressed.
    """
    if f is None or d is None or image_path is None:
        print("Parameter missing. Launching GUI...")
        launch_gui()
        return

    try:
        check_image_validity(image_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    print(f"Valori inseriti: {f}, {d}, {image_path}")

    compress(image_path, f, d)


def check_image_validity(image_path):
    """
    Checks if the image file exists and is a valid image.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    if not os.path.isfile(image_path):
        raise ValueError(f"{image_path} is not a valid file.")

    if not image_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        raise ValueError(f"The file {image_path} is not a valid image.")


if __name__ == "__main__":
    main()
