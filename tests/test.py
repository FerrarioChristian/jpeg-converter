import numpy as np

from converter import dct

TOLERANCE = 1e-2


def main():
    """Function to run the DCT tests."""
    print("Tolerance:", TOLERANCE)
    test_dct_1d()
    test_dct_2d()


def compare_results(actual, expected, tol, test_name):
    """Compares the actual and expected results of a test and prints the results."""
    relative_error = np.abs((actual - expected) / actual)
    max_error = np.max(relative_error)

    print(f"\n--- Test results: {test_name} ---")

    if np.all(relative_error < tol):
        print("✅ Test passed: All differences are within the tolerance.")
    else:
        print("❌ Test failed: Some differences exceed the tolerance.")

    print(f"Maximum relative error: {max_error:.2e}")
    print("\nActual result:")
    if actual.ndim > 1:
        np.set_printoptions(precision=2)
        print(actual)
    else:
        print(", ".join(f"{x:.2e}" for x in actual))

    print("\nExpected result:")
    if expected.ndim > 1:
        np.set_printoptions(precision=2)
        print(expected)
    else:
        print(", ".join(f"{x:.2e}" for x in expected))


def test_dct_1d():
    """Test of the DCT on a 1D array."""
    test_data = [231, 32, 233, 161, 24, 71, 140, 245]
    expected_result = np.array(
        [4.01e02, 6.60e00, 1.09e02, -1.12e02, 6.54e01, 1.21e02, 1.16e02, 2.88e01]
    )
    base = dct.dct_base(len(test_data))
    actual_result = dct.dct(test_data, base)
    compare_results(actual_result, expected_result, TOLERANCE, "DCT 1D")


def test_dct_2d():
    """Test of the DCT on a 2D array."""
    test_data = [
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228],
    ]
    expected_result = np.array(
        [
            [1.11e03, 4.40e01, 7.59e01, -1.38e02, 3.50e00, 1.22e02, 1.95e02, -1.01e02],
            [7.71e01, 1.14e02, -2.18e01, 4.13e01, 8.77e00, 9.90e01, 1.38e02, 1.09e01],
            [4.48e01, -6.27e01, 1.11e02, -7.63e01, 1.24e02, 9.55e01, -3.98e01, 5.85e01],
            [
                -6.99e01,
                -4.02e01,
                -2.34e01,
                -7.67e01,
                2.66e01,
                -3.68e01,
                6.61e01,
                1.25e02,
            ],
            [
                -1.09e02,
                -4.33e01,
                -5.55e01,
                8.17e00,
                3.02e01,
                -2.86e01,
                2.44e00,
                -9.41e01,
            ],
            [-5.38e00, 5.66e01, 1.73e02, -3.54e01, 3.23e01, 3.34e01, -5.81e01, 1.90e01],
            [
                7.88e01,
                -6.45e01,
                1.18e02,
                -1.50e01,
                -1.37e02,
                -3.06e01,
                -1.05e02,
                3.98e01,
            ],
            [
                1.97e01,
                -7.81e01,
                9.72e-01,
                -7.23e01,
                -2.15e01,
                8.13e01,
                6.37e01,
                5.90e00,
            ],
        ]
    )
    base2 = dct.dct_base(len(test_data))
    actual_result = dct.dct2(test_data, base2)
    compare_results(actual_result, expected_result, TOLERANCE, "DCT 2D")


if __name__ == "__main__":
    main()
