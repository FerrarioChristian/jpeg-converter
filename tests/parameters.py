from converter import compress

IMAGE = "./images/640x640.bmp"
F = [4, 8, 16, 32, 64, 128]

D = [1, 4, 8, 12, 16, 18, 24, 60]


def main():
    for f in F:
        d = int(f / 3)
        print(f"Processing with f={f}, d={d}")
        compress(IMAGE, f, d, "./results/parameters/f/f{}_d{}.bmp".format(f, d))
        print(f"Completed processing with f={f}, d={d}\n")

    f = 64
    for d in D:
        print(f"Processing with f={f}, d={d}")
        compress(IMAGE, f, d, "./results/parameters/d/d{}_f{}.bmp".format(d, f))
        print(f"Completed processing with f={f}, d={d}\n")


if __name__ == "__main__":
    main()
