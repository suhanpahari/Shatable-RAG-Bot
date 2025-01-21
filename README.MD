# Introducing Sha'table: A RAG Bot to Chat with Your Documents and URLs! 🚀
Say hello to **Sha'table**, your intelligent Retrieval-Augmented Generation (RAG) bot that bridges the gap between you and your data! Whether it's a document you've uploaded or a webpage URL, Sha'table empowers you to **converse seamlessly with your content**.

🗂️ **Upload Your Files**  
🌐 **Scrape and Chat with URLs**  
💡 **Get Instant Insights with Contextual Understanding**

Sha'table combines cutting-edge embeddings, vector databases, and machine learning to deliver accurate and context-aware responses to your queries. It's like having a personal assistant who knows your data inside out!

### Let Sha'table turn your static content into dynamic conversations! 🎉

![Image](https://github.com/user-attachments/assets/2f7d5d13-9c16-43d4-b26f-afeaec93006b)

---

## Project Overview

This project implements a Flask-based web application for managing and querying vectorized text data. Users can upload text files or provide URLs for scraping, which are then processed into vector embeddings and stored in a ChromaDB collection. The application also supports querying the stored data to retrieve the most relevant text chunks.

---

## Features

### 1. File Upload and Processing
- Upload `.txt` files via the web interface.
- Files are split into manageable chunks using the `detect_and_chunk_file` function.
- Each chunk is embedded using `get_embedding` and stored in a ChromaDB collection.

### 2. Web Scraping
- Scrape text from a given URL using `requests` and `BeautifulSoup`.
- Extracted text is saved and processed into vector embeddings.

### 3. Query Nearest Documents
- Query the vector database with a search string to retrieve the most relevant documents.
- Results are processed for enhanced readability using the `make_results_appropriate` function from `prepros.py`.

![Image](https://github.com/user-attachments/assets/500b7180-9870-49af-b0b4-1cecf51acfa2)

![Image](https://github.com/user-attachments/assets/ae9164c3-22d0-47f0-a065-bdbfdbe20303)


## Directory Structure
```
project-directory/
├── app.py                 # Main Flask application
├── encoding.py            # Handles file chunking
├── vector_11.py           # Embedding and vector database interactions
├── prepros.py             # Post-processing for query results
├── query.py               # Searches nearest cosin similariry chunk
├── check.py               # Check for a specific collection in Chroma DB
├── delete.py              # Delete collection in Chroma DB
├── scrp.py                # Scrape url and save into a txt file
├── main_11.py             # Main function for error handling in CLI
├── app.py                 # Flask app
├── uploads/               # Directory for uploaded and scraped files
│   └── temp.txt
├── templates/
│   └── index.html         # Revised HTML template for the web app
│   └── index2.html        # HTML template for the web app
└── requirements.txt       # Python dependencies
```

---

## API Endpoints

### 1. **Home**
- **Endpoint**: `/`
- **Method**: `GET`
- **Description**: Renders the home page.

### 2. **File Upload**
- **Endpoint**: `/upload`
- **Method**: `POST`
- **Payload**:
  - `file`: A `.txt` file to upload.
- **Response**:
  - **Success**: `{ "message": "File processed successfully", "collection": "<collection_name>" }`
  - **Error**: `{ "error": "<error_message>" }`

### 3. **Web Scraping**
- **Endpoint**: `/scrape`
- **Method**: `POST`
- **Payload**:
  - `url`: The URL to scrape text from.
- **Response**:
  - **Success**: `{ "message": "URL scraped and processed successfully", "collection": "<collection_name>" }`
  - **Error**: `{ "error": "<error_message>" }`

### 4. **Query Nearest Documents**
- **Endpoint**: `/query`
- **Method**: `POST`
- **Payload**:
  - `query`: The query text.
  - `collection_name`: Name of the collection to query.
- **Response**:
  - **Success**: `{ "documents": [...], "processed_results": [...] }`
  - **Error**: `{ "error": "<error_message>" }`

---

## Setup and Installation

### Prerequisites
- Python 3.10 recommended 
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/suhanpahari/Shatable-RAG-Bot.git
   cd project-directory
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the uploads directory:
   ```bash
   mkdir uploads
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Access the web app at: `http://127.0.0.1:5000/`

---

## Error Handling

### Common Errors
1. **Collection does not exist**:
   - **Cause**: Querying a collection that hasn’t been created.
   - **Solution**: Ensure the file or URL is processed successfully before querying.

2. **Invalid file type**:
   - **Cause**: Attempting to upload a file that is not `.txt`.
   - **Solution**: Upload only `.txt` files.

---
## Dependencies

Install dependencies from `requirements.txt`:
```plaintext
python-dotenv==1.0.1
chromadb==0.5.15
transformers==4.28.1
torch==1.13.1
flask==2.2.3
chardet==5.2.0
requests==2.28.1
beautifulsoup4==4.12.3
langchain-core==0.0.155  # Includes PromptTemplate, JsonOutputParser, OutputParserException
```

---

## Future Enhancements

1. Add support for additional file formats (e.g., `.pdf`, `.docx`).
2. Implement advanced query features, such as multi-document summarization.
3. Enhance the front-end with better visualization for query results.

---

## Author
Developed by [Soham Pahari](https://suhanxd.github.io/).

---

## License
This project is licensed under the MIT License.
