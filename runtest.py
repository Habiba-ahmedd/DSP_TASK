import numpy as np
from pathlib import Path

from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2


# =====================================================
# QUANTIZATION FUNCTION
# =====================================================

def quantize_signal(samples, levels):
    samples = np.array(samples, dtype=float)

    if len(samples) == 0:
        raise ValueError("The signal is empty.")

    if levels < 2:
        raise ValueError("Number of levels must be at least 2.")

    # Calculate minimum, maximum, and delta
    x_min = np.min(samples)
    x_max = np.max(samples)
    delta = (x_max - x_min) / levels

    if delta == 0:
        raise ValueError("Cannot quantize a constant signal.")

    # Calculate intervals and midpoints
    intervals = []
    midpoints = []

    for i in range(levels):
        start = x_min + i * delta
        end = x_min + (i + 1) * delta

        intervals.append((start, end))
        midpoints.append((start + end) / 2)

    # Quantize each sample
    indices = []
    encoded = []
    quantized = []
    errors = []

    bits = int(np.ceil(np.log2(levels)))

    for sample in samples:
        for i in range(levels):
            start, end = intervals[i]

            if start <= sample < end or i == levels - 1:
                indices.append(i + 1)
                encoded.append(format(i, f"0{bits}b"))
                quantized.append(midpoints[i])
                errors.append(midpoints[i] - sample)
                break

    # Calculate average quantization error power
    error_power = np.mean(np.array(errors) ** 2)

    return indices, encoded, quantized, errors, error_power


# =====================================================
# READ INPUT SIGNAL
# =====================================================

def read_test_samples(file_path):
    samples = []

    with open(file_path, "r") as file:
        # Skip the first 3 header lines
        for _ in range(3):
            file.readline()

        for line in file:
            line = line.strip()

            if line:
                parts = line.split()
                samples.append(float(parts[1]))

    return samples


# =====================================================
# TEST CASE 1 - 3 BITS = 8 LEVELS
# =====================================================

def run_test_case_1():
    print("\n========== TEST CASE 1 ==========")

    try:
        folder = Path(__file__).parent

        input_file = "G:\\dsp\project git\DSP_TASK\\testcases\Test 1\\Quan1_input.txt"
        output_file = "G:\\dsp\project git\DSP_TASK\\testcases\Test 1\\Quan1_Out.txt"

        samples = read_test_samples(input_file)

        indices, encoded, quantized, errors, error_power = (
            quantize_signal(samples, levels=8)
        )

        print("Running QuantizationTest1...")

        QuantizationTest1(
            str(output_file),
            encoded,
            quantized
        )

    except Exception as error:
        print("FAIL - Test Case 1:", error)


# =====================================================
# TEST CASE 2 - 4 LEVELS
# =====================================================

def run_test_case_2():
    print("\n========== TEST CASE 2 ==========")

    try:
        folder = Path(__file__).parent

        input_file = "G:\\dsp\project git\DSP_TASK\\testcases\Test 2\\Quan2_input.txt"
        output_file = "G:\\dsp\project git\DSP_TASK\\testcases\Test 2\\Quan2_Out.txt"

        samples = read_test_samples(input_file)

        indices, encoded, quantized, errors, error_power = (
            quantize_signal(samples, levels=4)
        )

        print("Running QuantizationTest2...")

        QuantizationTest2(
            str(output_file),
            indices,
            encoded,
            quantized,
            errors
        )

    except Exception as error:
        print("FAIL - Test Case 2:", error)


# =====================================================
# RUN ALL TESTS AUTOMATICALLY
# =====================================================

if __name__ == "__main__":
    run_test_case_1()
    run_test_case_2()