"""Task 4 static output checks using the supplied instructor reference files.

Expected values are read ONLY from the five reference .txt files; they are
never generated using the operations being tested.

IMPORTANT: Reference INPUT files were not supplied. Therefore this checks the
output against the selected reference, but cannot establish that the currently
loaded input is the input associated with that reference. For a valid official
test, load the matching instructor input before pressing Compute.
"""
from math import isclose
from pathlib import Path

from pathlib import Path

REFERENCE_DIR = Path(__file__).resolve().parent  / "testcases" / "Task5"

STATIC_REFERENCES = {
    ("Moving Average", 3): "MovingAvg_out1.txt",
    ("Moving Average", 5): "MovingAvg_out2.txt",
    ("First Derivative", None): "1st_derivative_out.txt",
    ("Second Derivative", None): "2nd_derivative_out.txt",
    ("Convolution", None): "Conv_output.txt",
}
# Moving-average expected values are rounded to three decimal places.
TOLERANCE = 0.0011


def load_expected_signal(filename):
    """Read instructor-format text: type, periodic, count, then index value."""
    lines = (REFERENCE_DIR / filename).read_text(encoding="utf-8-sig").splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    if len(lines) < 3:
        raise ValueError(f"Invalid reference file: {filename}")
    count = int(lines[2])
    if len(lines) - 3 != count:
        raise ValueError(f"Incorrect sample count in {filename}: {count} declared")
    indices, samples = [], []
    for line in lines[3:]:
        index, value = line.split()
        indices.append(int(index))
        samples.append(float(value))
    return indices, samples


def _same_numbers(actual, expected):
    return len(actual) == len(expected) and all(
        isclose(float(a), float(e), rel_tol=0.0, abs_tol=TOLERANCE)
        for a, e in zip(actual, expected)
    )


def check_task4_output(operation, input_indices, input_samples,
                       output_indices, output_samples, *,
                       window_size=None, second_indices=None, second_samples=None):
    """Compare computed output to the official static output; print PASS/FAIL."""
    key = (operation, window_size if operation == "Moving Average" else None)
    filename = STATIC_REFERENCES.get(key)
    print(f"\n[Task 4 Test] {operation}" +
          (f" | window={window_size}" if operation == "Moving Average" else ""), flush=True)
    if filename is None:
        print("NO MATCHING TEST: No supplied static reference for these settings.", flush=True)
        return "NO MATCHING TEST"

    try:
        expected_indices, expected_samples = load_expected_signal(filename)
    except (OSError, ValueError) as exc:
        print(f"TEST ERROR: Could not read {filename}: {exc}", flush=True)
        return "TEST ERROR"

    actual_indices = list(output_indices)
    actual_samples = list(output_samples)
    indices_ok = actual_indices == expected_indices
    samples_ok = _same_numbers(actual_samples, expected_samples)
    status = "PASS" if indices_ok and samples_ok else "FAIL"
    print(f"{status} | Reference: {filename}", flush=True)
    if status == "FAIL":
        print(f"  Expected indices: {expected_indices}", flush=True)
        print(f"  Actual indices:   {actual_indices}", flush=True)
        print(f"  Expected samples: {expected_samples}", flush=True)
        print(f"  Actual samples:   {actual_samples}", flush=True)
    return status


if __name__ == "__main__":
    print("Static reference files:")
    for key, filename in STATIC_REFERENCES.items():
        idx, vals = load_expected_signal(filename)
        print(f"{key}: {filename}, {len(vals)} samples, indices {idx[0]}..{idx[-1]}")
    print("Run an operation in the GUI to compare its computed output.")
