
import pandas as pd
import json
import ast
import uuid
from datetime import datetime


def create_report(patent_id, company, products): 
    report_id = uuid.uuid4()
    date = datetime.today().strftime('%Y-%m-%d')

    format = '''
        REPORT\n
        Analysis ID: {}\n
        Patent ID:  {}\n
        Company Name: {}\n
        Analysis Date: {}\n
    '''.format(report_id,patent_id,company,date)

    if products and len(products) > 0:
        format += "\n\n TOP INFRINGING PRODUCTS \n"

        for product in products:
            format += '''
                \nProduct Name: {}\n
                Infringement Likelhood: {}\n
                Relevant Claims: {}\n
                Explanation: {}\n
                Specific Features {}\n
            '''.format(product['product_name'], product['likelihood'], product['relevant_claims'], product['explanation'],product['specific_features'])
    return format


def fetch_products():
    # Load the COMPANY PRODUCT JSON data
    with open('company_products.json') as f:
        data = json.load(f)

    # Normalize the JSON to flatten nested structures
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

    # df['inventors'] = df['inventors'].apply(ast.literal_eval)
    # df_exploded = df.explode('inventors')
    # df = df_exploded


    # df['claims'] = df['claims'].apply(ast.literal_eval)
    # df_exploded = df.explode('claims')
    # df = df_exploded

    df = df.drop(['raw_source_url', 'image_urls', 'created_at', "updated_at", "landscapes", "provenance", "attachment_urls", "ai_summary", "raw_source_url", "priority_date", "application_events", "citations_non_patent" ], axis=1)
    return df