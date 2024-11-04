import streamlit as st
import data_helper
import os
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

gpt_template = """
    You are a helpful patent violation assistant that can help answer questions about patent data. 
    Answer the following question: {question}  
    By searching the following text: {patents}

    Only use the factual information from the texts to answer the question.
    If you dont feel like you have enough information to answer, say "I don't know."
    Your answers should be detailed. any lists you generate should be formatted with new line characters.
"""

# Set up the Streamlit app title and description
st.title("Patent Checker")
st.write("Check if you patent is infringed upon.")



patents = data_helper.fetch_patents()
products = data_helper.fetch_products()

with st.expander("Patents"):
    st.write(patents.tail(100))

with st.expander("Products"):
    st.write(products.tail(100))


key = "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"
# os.environ["PANDASAI_API_KEY"] = key
PANDASAI_API_KEY = key
format = '''
    Analysis ID: 
    Patent ID: 
    Company Name:
    Analysis Date:

    TOP INFRINGING PRODUCTS:
        Product Name: 
        Infringment Likelihood:
        Explanation:
        Specific Features:

'''

with st.form('my_form'):
    # Text input fields
    patent_id = st.text_input("Patent ID:")
    company = st.text_input("Company:")
    submitted = st.form_submit_button('Submit')

    if submitted and patent_id and company:
        patent = patents.loc[patent_id]
        company_products = products[products['company_name'].str.contains(company, case=False)]

        # st.write(patent)
        # st.write(company_products)
#     company_name = st.text_input("Company Name:")


        query = '''You are a mini-patent infringement check assistant bot. Patent infringement occurs when a party makes, uses, sells, or offers to sell a patented invention without
                permission from the patent holder. In essence, it means violating the exclusive rights granted to the patent
                owner, typically leading to legal disputes.

                Can you tell me which of these products in this dataframe: {company_products}
                Might infringe on this patent {patent}
                find the top two infringing products of the company.
                and generate explanations of why these products potentially infringe the patent, specifically detailing which claims are at issue.
               
                Return your result using this format, fill in the blanks where needed: {format}
                '''

        llm = OpenAI(api_token=PANDASAI_API_KEY)    
        query_engine = SmartDataframe(patent, company_products, config={"llm":llm})

        answer = query_engine.chat(query)

        st.write(answer)