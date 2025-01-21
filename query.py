from vector_11 import collection
from vector_11 import get_embeddings

def get_nearest_result(query_text, n=1):
   query_embedding = get_embeddings([query_text])[0]
   
   results = collection.query(
       query_embeddings=[query_embedding],
       n_results=n
   )
   
   return results['documents'], results['metadatas']

def nearest_documents(query_text):
   return get_nearest_result(query_text)