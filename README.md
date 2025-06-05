# DCT2 based image compression

>This project is a simplified simulation of JPEG-style image compression based on the 2D Discrete Cosine Transform (DCT2), implemented for grayscale `.bmp` images. It was developed as part of a university assignment in scientific computing.

---

## Features

- Manual implementation of the 2D DCT (DCT2) from theoretical definition.
- Performance comparison between manual and library-based DCT2 using SciPy (FFT-based).
- Block-wise image compression using DCT2 and high-frequency suppression.
- GUI or CLI for image selection and parameter tuning.
- Side-by-side visualization of original and compressed images.

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
To run the GUI for image selection and compression parameters, you can use:
```bash
run-gui # This will open the GUI for image selection and compression parameters
```
or 
```bash
python main.py
```
The compressed image will be displayed next to the original, and saved to the results/ folder.
> [!WARNING]
> To run the GUI, ensure you have the `tkinter` library installed. If not, you can install it using your package manager (e.g., `apt-get install python3-tk` on Debian-based systems).

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
