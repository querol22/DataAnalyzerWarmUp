# analyzer.py
"""
A simple warm-up script for data analysis.
"""

def analyze_numbers(numbers):
    """Return the mean and maximum of a list of numbers."""
    if not numbers:
        return None, None
    mean_val = sum(numbers) / len(numbers)
    max_val = max(numbers)
    return mean_val, max_val


if __name__ == "__main__":
    data = [10, 20, 30, 40, 50]
    mean, max_val = analyze_numbers(data)
    print(f"Data: {data}")
    print(f"Mean: {mean}")
    print(f"Max: {max_val}")
