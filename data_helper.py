
import pandas as pd
import json
from datetime import datetime

def generate_likelihood(similarity_score):
    if similarity_score < 0.2:
        likelihood = "High"
    elif similarity_score < 0.5:
        likelihood = "Medium"
    else:
        likelihood = "Low"
    return likelihood 


def fetch_products():
    # Load the COMPANY PRODUCT JSON data
    with open('company_products.json') as f:
        data = json.load(f)

    products_df = pd.json_normalize(data, record_path=['companies', 'products'], meta=[['companies', 'name']])

    # Rename columns for clarity
    products_df.columns = ['product_name', 'description', 'company_name']
    products_df = products_df.astype(str)
    return products_df


def fetch_patents():
    # Load the PATENTS JSON file
    with open('patents.json') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = df.drop(['raw_source_url', 'image_urls', 'created_at', "updated_at", "landscapes", "provenance", "attachment_urls", "ai_summary", "raw_source_url", "priority_date", "application_events", "citations_non_patent" ], axis=1)
    return df

def extract_claims(patents):
    claims_data = []
    for _, row in patents.iterrows():
        claims_list = json.loads(row["claims"]) # load in claims json fields
        for claim in claims_list:
            claims_data.append({
                "publication_number": patents["publication_number"],
                "claim_number": claim["num"],
                "claim_text": claim["text"]
            })
    df_claims = pd.DataFrame(claims_data)
    return df_claims
