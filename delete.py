import chromadb
from vector_11 import collection

# Initialize Chroma client
client = chromadb.Client()

# Delete the collection
client.delete_collection(name="test2_collection")

print("Collection 'test2_collection' deleted.")