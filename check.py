# Load ChromaDB Client
from chromadb.config import Settings
from chromadb import Client
from vector_11 import collection

client = Client(Settings())

def list_all_collections():
    """List all collections in ChromaDB."""
    collections = client.list_collections()
    if not collections:
        print("No collections found in ChromaDB.")
    else:
        print("Available collections:")
        for coll in collections:
            print(f"- {coll.name}")

def verify_saved_embeddings(collection_name):
    """Retrieve and print the contents of a ChromaDB collection."""
    try:
        collection = client.get_collection(name=collection_name)
        documents = collection.get(include=['documents', 'metadatas', 'embeddings'])
        
        if not documents['documents']:
            print(f"No embeddings found in the collection '{collection_name}'.")
        else:
            print(f"Collection '{collection_name}' contains the following data:")
            for doc, meta in zip(documents['documents'], documents['metadatas']):
                print(f"Document: {doc}")
                print(f"Metadata: {meta}")
                print("\n")
            print(f"Total embeddings: {len(documents['documents'])}")
    except Exception as e:
        print(f"Error accessing collection '{collection_name}': {e}")

# List all available collections to verify the correct collection name
list_all_collections()

# Update this with the collection name used for your file
collection_name = "test2_collection"  # Replace with the actual collection name for the different file

# Verify embeddings for the specified collection
verify_saved_embeddings(collection_name)