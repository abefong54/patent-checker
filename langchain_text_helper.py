
import openai

FORMAT = """ 
Analysis ID: [generate an id for this report]
Date : add todays in YYYY-MM-DD format
[a short explanation as to why there is an infringment]
\nRelevant Claims : [provide a list of claim numbers from the claims provided that were infringed upon, make sure the claim numbers all have the same formatting,remove all leading zeros if needed. return the number only]
\nSpecific Features : provide a dotted list from the features given that cause the infringments
"""


def llm_generate_infringement_explanation(patent_claims, patent_description, patent_abstract, app_features):
    prompt = (
        f"You are an expert in patent analysis. Given the following patent claims, description, and abstract:\n"
        f"Claims: {patent_claims}\n"
        f"Description: {patent_description}\n"
        f"Abstract: {patent_abstract}\n\n"
        f"And given the description of a product:\n"
        f"Features: {app_features}\n\n"
        f"Explain briefly why this product might be infringing on the patent claims and return your answer in the following format: {FORMAT}"
    )

    # Use openai.Chat.create to generate the response
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature = 0,
        max_tokens=200,
    )
    
    explanation = response.choices[0].text
    return explanation

