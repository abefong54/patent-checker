
import faiss
import numpy as np
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4

def generate_likelihood(similarity_score):
    if similarity_score < 0.2:
        likelihood = "High"
    elif similarity_score < 0.5:
        likelihood = "Medium"
    else:
        likelihood = "Low"
    return likelihood 

def generate_report(patents, company_products):
        patents['text'] = patents["publication_number"] + " : " + patents["description"] + " : " + patents["claims"]  + " : " + patents["abstract"]
        company_products['text'] = company_products['product_name'] + " : " + company_products['description']

        # Initialize the embedding model
        embedding_model = OpenAIEmbeddings()

        # Convert patent and app text to embeddings
        patent_texts = patents["text"].tolist()
        app_texts = company_products["text"].tolist()


        # Embed patent and app texts
        patent_embeddings = embedding_model.embed_documents(patent_texts)
        app_embeddings = embedding_model.embed_documents(app_texts)

        # Initialize FAISS index with the embedding dimension
        dimension = len(patent_embeddings[0])
        faiss_index = faiss.IndexFlatL2(dimension)

        # Add app embeddings to FAISS
        app_embedding_matrix = np.array(app_embeddings)
        faiss_index.add(app_embedding_matrix)

        # Set number of top matches to retrieve
        top_k = 2

        # Iterate over each patent embedding
        for i, patent_embedding in enumerate(patent_embeddings):
            # Reshape patent embedding for searching
            patent_embedding = np.array([patent_embedding])
            
            # Search for top 2 closest app embeddings
            distances, indices = faiss_index.search(patent_embedding, top_k)
            
       