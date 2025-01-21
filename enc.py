import chardet

def detect_file_encoding(file_path):
  """
  Detects the encoding of a given file.

  Args:
    file_path: Path to the file.

  Returns:
    The detected encoding of the file.
  """

  with open(file_path, 'rb') as f:
    rawdata = f.read()
    result = chardet.detect(rawdata)
    return result['encoding']

# Example usage:
file_path = 'uploads\Medium_(website).txt'  # Replace with the actual file path
encoding = detect_file_encoding(file_path)
print(f"Detected encoding: {encoding}")