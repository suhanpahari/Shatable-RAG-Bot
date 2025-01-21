
'''def process_chunks_to_vectordb(chunks):
    # Example: Store chunks in a vector database
    for i, chunk in enumerate(chunks):
        # Perform vectorization logic (e.g., using embeddings)
        vector = vectorize_text(chunk)
        store_in_vectordb(i, vector)

def vectorize_text(text):
    # Example: Dummy vectorization
    return [ord(char) for char in text]

def store_in_vectordb(index, vector):
    # Example: Simulated storage
    print(f"Stored vector for chunk {index} in VectorDB")
import chromadb
from transformers import BertTokenizer, BertModel
import torch
from pathlib import Path
from encoding import chunks

# Initialize BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()  # Set to evaluation mode

# Initialize ChromaDB
client = chromadb.Client()

# Create collection using the source file name (assuming chunks are from test.txt)
collection = client.create_collection(name="test")

# Function to get embeddings for a single chunk
def get_embedding(chunk):
    with torch.no_grad():
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

# Process each chunk and add to ChromaDB
for i, chunk in enumerate(chunks):
    # Get embedding for the chunk
    embedding = get_embedding(chunk)
    
    # Add to ChromaDB
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[{"index": i}],
        ids=[str(i)]
    )

print(f"Successfully processed {len(chunks)} chunks and added to ChromaDB.")'''

import chromadb
from transformers import BertTokenizer, BertModel
import torch
from pathlib import Path

# Initialize BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()  # Set to evaluation mode

# Initialize ChromaDB
client = chromadb.Client()

# Function to get embeddings for a single chunk
def get_embedding(chunk):
    with torch.no_grad():
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
