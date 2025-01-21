import chromadb
from vector_11 import collection


client = chromadb.Client()


collections = client.list_collections()


for collection in collections:
    print(f"Collection name: {collection.name}")
