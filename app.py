import streamlit as st
import data_helper
import os
from uuid import uuid4
import openai
import faiss
import numpy as np
import json
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain_core.documents import Document
from fpdf import FPDF

def generate_likelihood(similarity_score):
    if similarity_score < 0.2:
        likelihood = "High"
    elif similarity_score < 0.5:
        likelihood = "Medium"
    else:
        likelihood = "Low"
    return likelihood 

def create_report(distances,indices,top_matches,explanation):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
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
    # Title for the report
    pdf.cell(200, 10, txt="Patent Infringement Analysis Report", ln=True, align="C")
    pdf.cell(200, 10, txt="Patent: " + patent_id, ln=True, align="C")
    pdf.cell(200, 10, txt="Company: " + company, ln=True, align="C")

    pdf.ln(10)
    # Iterate over top matches and generate explanations
    for match in top_matches:
        patent_number = match["patent_number"]
        app_name = match["app_name"]
        company_name = match["company_name"]
        likelihood = match["likelihood"]
        similarity_score = match["similarity_score"]
        app_features = match["app_features"]

        # Display information for each infringing product
        pdf.multi_cell(0,10,f"### App Name: {app_name}")
        pdf.multi_cell(0,10,f"- **Company Name**: {company_name}")
        pdf.multi_cell(0,10,f"- **Likelihood of Infringement**: {likelihood}")
        pdf.multi_cell(0,10,f"- **Explanation**:\n {explanation}")
        pdf.multi_cell(0,10,f"---")
        pdf.ln(10)  # Add a blank line between sections
    
    return pdf



def visualize_report(distances,indices,top_matches):
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
        patent_number = match["patent_number"]
        app_name = match["app_name"]
        company_name = match["company_name"]
        likelihood = match["likelihood"]
        similarity_score = match["similarity_score"]
        app_features = match["app_features"]

        # Get patent details for the current patent
        patent_info = patents[patents["publication_number"] == patent_number].iloc[0]
        patent_claims = patent_info["claims"]
        patent_description = patent_info["description"]

        # Generate explanation using LLM chain
        explanation = generate_infringement_explanation(patents['claims'], patents['description'], patents['abstract'], app_features)

        # Display information for each infringing product
        st.write(f"### App Name: {app_name}")
        st.write(f"- **Company Name**: {company_name}")
        st.write(f"- **Likelihood of Infringement**: {likelihood}")
        st.write(f"- **Explanation**:\n {explanation}")   
        st.write("---")
    

# Set up the Streamlit app title and description
st.title("Patent Checker")
st.write("Check if you patent is infringed upon.")

format = """ 
[a short explanation as to why there is an infringment]\n
Key Features: [a dotted list of features that cause the infringment] \n
Claims : [provide a list of claim numbers from the claims provided that were infringed upon, do not modify the format of those numbers, just select and return the number only]
"""
# Define the chat input manually
def generate_infringement_explanation(patent_claims, patent_description, patent_abstract, app_features):
    prompt = (
        f"You are an expert in patent analysis. Given the following patent claims, description, and abstract:\n"
        f"Claims: {patent_claims}\n"
        f"Description: {patent_description}\n"
        f"Abstract: {patent_abstract}\n\n"
        f"And given the description of a product:\n"
        f"Features: {app_features}\n\n"
        f"Explain briefly why this product might be infringing on the patent claims and return your answer in the following format: {format}"
        # f"Key Features: - feature 1\n -feature2\n "
        # f"Also provide a list of claim numbers from the claims provided that were infringed upon, do not modify the format of those numbers, just select and return the number only."
        # f"at the end of your explanation return that list in this format: Claims: [list of all the claim numbers]"
    )

    # Use openai.Chat.create to generate the response
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature = 0,
        max_tokens=200,
    )
    
    # Extract and return the generated explanation
    # print(response)
    explanation = response.choices[0].text
    return explanation


patents = data_helper.fetch_patents()
products = data_helper.fetch_products()
report = None

key = "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"
os.environ["OPENAI_API_KEY"] = key

with st.form('my_form'):
    # Text input fields
    # patent_id = st.text_input("Patent ID:")
    # company = st.text_input("Company:")
    patent_id = "US-RE49889-E1"
    company = "Walmart"
    submitted = st.form_submit_button('Submit')

    if submitted and patent_id and company:
        patents = patents[patents['publication_number'] == patent_id]
        company_products = products[products['company_name'].str.contains(company, case=False)]
        # Parse the JSON strings and flatten the claims data
        claims_data = []
        for _, row in patents.iterrows():
            claims_list = json.loads(row["claims"])  # Parse JSON string to list of dictionaries
            
            for claim in claims_list:
                claims_data.append({
                    "publication_number": patent_id,
                    "claim_number": claim["num"],
                    "claim_text": claim["text"]
                })

        # Create a new DataFrame with flattened claims
        df_claims = pd.DataFrame(claims_data)
        
        # st.write(patents)
        # st.write(company_products)
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
            top_matches = []

            # report = create_report(distances,indices,top_matches)
            visualize_report(distances,indices,top_matches)


          
# if report:
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     st.download_button(
#         label="Download Report as Text File",
#         data=report_content,
#         file_name="patent_infringement_report.txt",
#         mime="text/plain"
# )