import os
from pathlib import Path
import logging
from encoding import detect_and_chunk_file
from vector_11 import client, tokenizer, model, get_embedding
from prepros import make_results_appropriate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_nearest_result(query_text, collection, n=1):
    query_embedding = get_embedding(query_text)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n
    )
    
    return results['documents'], results['metadatas']

def nearest_documents(query_text, collection):
    return get_nearest_result(query_text, collection)

def main(file_path):
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.is_file():
            raise ValueError(f"{file_path} is not a valid file.")
            
        chunks = detect_and_chunk_file(file_path)
        logger.info(f"File processed into {len(chunks)} chunks")
        if chunks:
            logger.debug(f"Sample of first chunk: {chunks[0][:100]}...")

        collection_name = file_path.stem
        try:
            collection = client.create_collection(name=collection_name)
            logger.info(f"Created new collection: {collection_name}")
        except ValueError:
            collection = client.get_collection(name=collection_name)
            logger.info(f"Using existing collection: {collection_name}")

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"index": i, "source": str(file_path)}],
                ids=[str(i)]
            )
            
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1} chunks...")
                
        logger.info(f"Successfully processed all {len(chunks)} chunks into vector database!")
        
        query_text = input("Enter your query: ")
        
        documents, metadatas = nearest_documents(query_text, collection)
        
        processed_results = make_results_appropriate(query_text, documents)
        logger.info(f"{processed_results}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        file_path = "uploads/Mediumwebsite.txt"
        main(file_path)
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")