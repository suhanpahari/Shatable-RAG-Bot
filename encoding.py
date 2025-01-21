'''import chardet

def detect_and_chunk_file(file_path, chunk_size=200):
    # Detect file encoding
    with open(file_path, "rb") as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    file_encoding = result['encoding']
    
    # Open the file using the detected encoding
    with open(file_path, "r", encoding=file_encoding) as file:
        text = file.read()
    
    # Split text into chunks
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks'''

import chardet

def detect_and_chunk_file(file_path, chunk_size=700):
    
    with open(file_path, "rb") as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    file_encoding = result['encoding']
    
    
    with open(file_path, "r", encoding=file_encoding) as file:
        text = file.read()
    
    
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks