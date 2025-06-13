# DCT2 based image compression

>This project is a simplified simulation of JPEG-style image compression based on the 2D Discrete Cosine Transform (DCT2), implemented for grayscale `.bmp` images. It was developed as part of a university assignment in scientific computing.

---

## Features

- Manual implementation of the 2D DCT (DCT2) from theoretical definition.
- Performance comparison between manual and library-based DCT2 using SciPy (FFT-based).
- Block-wise image compression using DCT2 and high-frequency suppression.
- **Modern Dark-Mode GUI** powered by `customtkinter` for parameter tuning and side-by-side visualization.
- **Quantitative Quality Metrics:** Real-time calculation of **PSNR** (Peak Signal-to-Noise Ratio) and **MSE** (Mean Squared Error).
- **Theoretical File Size Estimation (Huffman):** Simulates Huffman Encoding on the quantized DCT coefficients to provide an accurate estimate of the final compressed file size. This can be toggled on/off to compare the theoretical size with the raw uncompressed `.bmp` size.
- **Visual Error Map:** Generates a heatmap showing exactly which high-frequency details were discarded during compression, complete with an intuitive 0-255 colorbar legend.
- **Interactive Zoom:** A pixel-perfect magnification tool (nearest-neighbor scaling) that lets you click and drag to explore the 400% zoomed image and clearly observe the 8x8 blocking artifacts typical of DCT compression.
- **Compare Mode:** A presentation-ready full-screen view that overlays the original and compressed images, letting you drag a vertical divider left and right to interactively compare the before and after results.
- **Fullscreen Image Toggle:** Click on any image in the side-by-side view to instantly enlarge it for detailed inspection.

## Objectives

- Understand and implement the mathematical definition of DCT and DCT2.
- Explore the effect of frequency-based compression on image quality.
- Analyze how the choice of block size `F` and frequency threshold `D` affects compression.
- Compare naive and optimized algorithms in terms of performance and scalability.


## Installation

This project uses Python 3 and open-source libraries only.

### 1. Clone the repository

```bash
git clone https://github.com/FerrarioChristian/jpeg-converter.git
cd jpeg-converter
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -e .
```

## Usage

You can run the compressor via command-line or GUI, depending on your implementation.

### Command-Line Interface (CLI)
```bash
python main.py --image path/to/image.bmp -f 8 -d 8
```

### Graphical User Interface (GUI)
To run the modern GUI for image selection and compression parameters, use:
```bash
run-gui # This will open the GUI for image selection and compression parameters
```
or 
```bash
python main.py
```
The GUI provides a complete visual case study platform where you can:
- Adjust `D` (frequencies kept) dynamically using a slider bound by `2F - 2`.
- Toggle the **Huffman Size Estimation** to calculate exact compression entropy.
- View the percentage of retained frequencies in real-time.
- Compare original and compressed images side-by-side (click any image to enlarge it).
- Review PSNR, MSE, and estimated file sizes at a glance.
- Click **"Show Error Map"** to see a heatmap (with a color legend) of the discarded high-frequency data.
- Click **"Zoom"** to pan around a 400% magnified view of the compressed image to easily spot 8x8 blocking artifacts.
- Click **"Compare Mode"** in the top right to enter a full-screen interactive before/after slider mode (Press ESC to exit).

## Benchmarking
To run the benchmark and generate the timing plot comparing your custom DCT2 with the SciPy version:
```bash
python tests/benchmark.py
```
or
```bash
run-benchmark
```
This will generate a semilogarithmic plot saved in results/benchmark.jpeg

## Test
To run the test to verify the correctness of the algorithm:
```bash
python tests/test.py
```
or
```bash
run-test
```



### Notes
- Only grayscale .bmp images are supported.
- Frequencies are discarded based on the rule: keep all DCT coefficients cₖₗ such that `k + l < d`.
- Block remainders at the image borders are discarded for simplicity.

## Project Structure
```
├── cli
│   ├── __init__.py
│   └── cli.py
├── converter
│   ├── __init__.py
│   ├── backend.py
│   └── dct.py
├── gui
│   ├── __init__.py
│   ├── gui.py
│   └── resources
│       └── caravaggio.jpg
├── images
├── main.py
├── pyproject.toml
├── results
│   ├── benchmark.jpeg
│   └── result.bmp
└── tests
    ├── __init__.py
    ├── benchmark.py
    └── test.py
```
