
import pandas as pd
import json
import ast


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

    # Normalize the JSON to flatten nested structures
    df = pd.json_normalize(data)

    # Convert the 'inventors' column from JSON string to list of dictionaries
    df['inventors'] = df['inventors'].apply(ast.literal_eval)

    # Expand inventors into separate rows
    inventors_df = df.explode('inventors')

    # Reset the index of both DataFrames before concatenating
    inventors_df = inventors_df.reset_index(drop=True)
    df = df.reset_index(drop=True)

    inventors_df = pd.concat([inventors_df.drop(columns=['inventors']),
                            pd.json_normalize(inventors_df['inventors'])], axis=1)
    # Group inventors by patent 'id' and aggregate as a list of dictionaries
    inventors_grouped = inventors_df.groupby('id')[['first_name', 'last_name']].apply(lambda x: x.to_dict('records')).reset_index()

    # Rename the column to indicate it's a list of inventors
    inventors_grouped.columns = ['id', 'inventors']

    # Merge this grouped data back into the main DataFrame 'df'
    df = df.merge(inventors_grouped, on='id', how='left')
    df.set_index('publication_number', inplace=True)
    df = df.astype(str)
    return df