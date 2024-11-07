import streamlit as st
import data_helper as dh
import langchain_text_helper as lh
import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings

# Set up the Streamlit app title and description
st.title("Patent Checker")
st.write("Check if you patent is infringed upon.")

key = "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"
top_k = 2

# Define the chat input manually
os.environ["OPENAI_API_KEY"] = key

def main():
    patents_df = dh.fetch_patents()
    products_df = dh.fetch_products()


    create_form(patents_df, products_df)

def create_text_embeddings_for_faiss(patent_id, company, patents_df, products_df):
    patents = patents_df[patents_df['publication_number'] == patent_id]
    company_products = products_df[products_df['company_name'].str.contains(company, case=False)]

    patents['text'] = patents["publication_number"] + " : " + patents["description"] + " : " + patents["claims"]  + " : " + patents["abstract"]
    company_products['text'] = company_products['product_name'] + " : " + company_products['description']

    # Initialize the embedding model
    embedding_model = OpenAIEmbeddings()

    # Convert patent and app text to embeddings
    patent_texts = patents["text"].tolist()
    app_texts = company_products["text"].tolist()
    patent_embeddings = embedding_model.embed_documents(patent_texts)
    app_embeddings = embedding_model.embed_documents(app_texts)
    dimension = len(patent_embeddings[0])
    faiss_index = faiss.IndexFlatL2(dimension)

    # Add app embeddings to FAISS
    app_embedding_matrix = np.array(app_embeddings)
    faiss_index.add(app_embedding_matrix)

    return faiss_index, patent_embeddings, company_products

def create_form(patents, products):  
    with st.form('my_form', border=True):
        with st.sidebar:
            patent_id = st.text_input("Patent ID:")
            company = st.text_input("Company:")
            submitted = st.form_submit_button('Submit')
        if submitted and patent_id and company:
            faiss_index, patent_embeddings,company_products = create_text_embeddings_for_faiss(patent_id=patent_id, company=company, patents_df=patents, products_df=products)
            for _, patent_embedding in enumerate(patent_embeddings):
                patent_embedding = np.array([patent_embedding])
                distances, indices = faiss_index.search(patent_embedding, top_k)
                generate_report(distances,indices,patents,company_products, patent_id, company)
            

def generate_report(distances,indices,patents, company_products,patent_id,company):
    top_matches = []
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        app_info = company_products.iloc[idx]
        likelihood = "High" if dist < 0.5 else "Medium" if dist < 0.3 else "Low"
        top_matches.append({
            "patent_number": patent_id,
            "app_name": app_info["product_name"],
            "company_name": company,
            "likelihood": likelihood,
            "similarity_score": dist,
            "app_features": app_info["description"]
        })

    # Display report in Streamlit
    st.title("Patent Infringement Analysis Report")
    st.subheader("Patent: " + patent_id)
    st.subheader("Company: " + company , divider=True)
    
    # Iterate over top matches and generate explanations
    for match in top_matches:
        app_name = match["app_name"]
        company_name = match["company_name"]
        likelihood = match["likelihood"]
        app_features = match["app_features"]

        # Generate explanation using LLM chain
        explanation = lh.llm_generate_infringement_explanation(patents['claims'], patents['description'], patents['abstract'], app_features)


        # Display information for each infringing product
        st.write(f"### App Name: {app_name}")
        st.write(f"- **Company Name**: {company_name}")
        st.write(f"- **Likelihood of Infringement**: {likelihood}")
        st.write(f"- **Explanation**:\n {explanation}")   
        st.write("---")
    return 
    


main()