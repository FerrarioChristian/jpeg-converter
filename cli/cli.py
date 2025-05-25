import argparse


def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        type=int,
        const=8,
        default=None,
        nargs="?",
        help="Number F that represents the size of the blocks (default: 8)",
    )
    parser.add_argument(
        "-d",
        type=int,
        const=8,
        nargs="?",
        default=None,
        help="Number D that represents the frequency up to which the image is cut (default: 8)",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="?",
        const="./images/640x640.bmp",
        default=None,
        help="Path to the input image (default: ./images/640x640.bmp)",
    )
    return parser.parse_args()


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
