from converter import compress

IMAGED = "./images/640x640.bmp"
IMAGEF = "./images/deer.bmp"
F = [8, 16, 32, 64, 128]

D = [1, 4, 8, 12, 16, 18, 24, 60]


def main():
    for f in F:
        d = int(f / 5)
        print(f"Processing with f={f}, d={d}")
        compress(IMAGEF, f, d, "./results/parameters/f/f{}_d{}.jpg".format(f, d))
        print(f"Completed processing with f={f}, d={d}\n")

    f = 64
    for d in D:
        print(f"Processing with f={f}, d={d}")
        compress(IMAGED, f, d, "./results/parameters/d/d{}_f{}.jpg".format(d, f))
        print(f"Completed processing with f={f}, d={d}\n")


if __name__ == "__main__":
    main()
