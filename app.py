
'''
from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import logging
from encoding import detect_and_chunk_file
from vector_11 import client, tokenizer, model, get_embedding
from prepros import make_results_appropriate  # Import the function from prepros.py

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

# File upload directory
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to retrieve the nearest result
def get_nearest_result(query_text, collection, n=1):
    query_embedding = get_embedding(query_text)  # Embedding for the single query
    results = collection.query(
        query_embeddings=[query_embedding],  # The query embedding
        n_results=n  # Number of nearest results to retrieve
    )
    return results['documents'], results['metadatas']

def nearest_documents(query_text, collection):
    return get_nearest_result(query_text, collection)

def process_file(file_path):
    try:
        # Validate file path
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"{file_path} is not a valid file.")
        
        # Process the file using encoding.py
        chunks = detect_and_chunk_file(file_path)
        logger.info(f"File processed into {len(chunks)} chunks")
        
        if chunks:
            logger.debug(f"Sample of first chunk: {chunks[0][:100]}...")  # Show first 100 chars of first chunk
        
        # Create collection using the file name
        collection_name = file_path.stem
        try:
            collection = client.create_collection(name=collection_name)
            logger.info(f"Created new collection: {collection_name}")
        except ValueError:
            collection = client.get_collection(name=collection_name)
            logger.info(f"Using existing collection: {collection_name}")
        
        # Process chunks and add to ChromaDB
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"index": i, "source": str(file_path)}],
                ids=[str(i)]
            )
            
            # Log progress every 10 chunks
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1} chunks...")
        
        logger.info(f"Successfully processed all {len(chunks)} chunks into vector database!")
        
        return collection
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        # If no file is selected or file type is invalid
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "No file selected or invalid file type"}), 400
        
        # Save the file to the uploads directory
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Process the uploaded file
        collection = process_file(file_path)
        
        return jsonify({"message": "File processed successfully", "collection": collection.name}), 200

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/query', methods=['POST'])
def query_nearest_documents():
    try:
        query_text = request.json.get('query')
        collection_name = request.json.get('collection_name')
        
        # Validate input
        if not query_text or not collection_name:
            return jsonify({"error": "Missing query or collection name"}), 400
        
        collection = client.get_collection(name=collection_name)
        documents, metadatas = nearest_documents(query_text, collection)
        
        # Process the results using prepros.py
        processed_results = make_results_appropriate(query_text, documents)
        
        return jsonify({"documents": documents, "processed_results": processed_results}), 200
    
    except Exception as e:
        logger.error(f"Error in querying documents: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

    '''

from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import logging
from encoding import detect_and_chunk_file
from vector_11 import client, tokenizer, model, get_embedding
from prepros import make_results_appropriate  
import requests
from bs4 import BeautifulSoup
import re
import atexit  
import shutil  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_nearest_result(query_text, collection, n=1):
    query_embedding = get_embedding(query_text)  
    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=n  # Number of nearest results to retrieve
    )
    return results['documents'], results['metadatas']

def nearest_documents(query_text, collection):
    return get_nearest_result(query_text, collection)

def process_file(file_path):
    try:
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"{file_path} is not a valid file.")
        
        
        chunks = detect_and_chunk_file(file_path)
        logger.info(f"File processed into {len(chunks)} chunks")
        
        if chunks:
            logger.debug(f"Sample of first chunk: {chunks[0][:100]}...")  # Show first 100 chars of first chunk
        
        # Create collection using the file name
        collection_name = file_path.stem
        try:
            collection = client.create_collection(name=collection_name)
            logger.info(f"Created new collection: {collection_name}")
        except ValueError:
            collection = client.get_collection(name=collection_name)
            logger.info(f"Using existing collection: {collection_name}")
        
        # Process chunks and add to ChromaDB
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
        
        return collection
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

# Function to clean up files 
def cleanup_on_exit():
    try:
        
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Delete the file
                        logger.info(f"Deleted file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Delete subdirectories (if any)
                        logger.info(f"Deleted directory: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete {file_path}: {str(e)}")
            logger.info("All files in the uploads folder have been deleted.")
        
        # Delete all collections 
        collections = client.list_collections()
        for collection in collections:
            client.delete_collection(name=collection.name)
            logger.info(f"Deleted ChromaDB collection: {collection.name}")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")


atexit.register(cleanup_on_exit)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "No file selected or invalid file type"}), 400
        
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        
        collection = process_file(file_path)
        
        return jsonify({"message": "File processed successfully", "collection": collection.name}), 200

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/scrape', methods=['POST'])
def scrape_url():
    try:
        url = request.json.get('url')
        
        
        if not url:
            return jsonify({"error": "Missing URL"}), 400
        
        
        response = requests.get(url)
        response.raise_for_status()  
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        text = soup.get_text()
        
        
        file_name = url.split('/')[-1]  
        file_name = re.sub(r'[^\w\-.]', '', file_name)  
        file_name = file_name[:50]  
        file_name += '.txt' 
        
        
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        
        collection = process_file(file_path)
        
        return jsonify({"message": "URL scraped and processed successfully", "collection": collection.name}), 200
    
    except Exception as e:
        logger.error(f"Error scraping URL: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/query', methods=['POST'])
def query_nearest_documents():
    try:
        query_text = request.json.get('query')
        collection_name = request.json.get('collection_name')
        
        # Validate input
        if not query_text or not collection_name:
            return jsonify({"error": "Missing query or collection name"}), 400
        
        collection = client.get_collection(name=collection_name)
        documents, metadatas = nearest_documents(query_text, collection)
        
        
        processed_results = make_results_appropriate(query_text, documents)
        
        return jsonify({"documents": documents, "processed_results": processed_results}), 200
    
    except Exception as e:
        logger.error(f"Error in querying documents: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)