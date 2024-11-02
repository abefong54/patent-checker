import streamlit as st

# Set up the Streamlit app title and description
st.title("Patent Checker")
st.write("Check if you patent is infringed upon.")

# Text input fields
input_1 = st.text_input("Patent ID:")
input_2 = st.text_input("Company Name:")

# Display the entered text
if st.button("Submit"):
    st.write("You entered:")
    st.write(f"First Input: {input_1}")
    st.write(f"Second Input: {input_2}")


# consider using langchain embeddings to learn from the json files 
# and then generate the required report

# https://github.com/abefong54/youtube_assistant_llm/blob/main/langchain_text_helper.py