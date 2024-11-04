# from langchain.document_loaders import YoutubeLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.llms import OpenAI
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.vectorstores import FAISS # Library from META for efficient similarity search
# # from dotenv import load_dotenv
# import openai
# import os
# # load_env()

# embeddings = OpenAIEmbeddings()
# os.environ['OPENAI_API_KEY'] = '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'
# query = "what is this data about?"

# gpt_template = """
#     You are a helpful research assistant that can help answer questions based on the transcript from two different texts. 
#     Answer the following question: {question}  
#     By searching the following text: {doc_one}
#     and comparing with the following text: {doc_two}

#     Only use the factual information from the texts to answer the question.
#     If you dont feel like you have enough information to answer, say "I don't know."
#     Your answers should be detailed. any lists you generate should be formatted with new line characters.
# """

# def create_similarity_embedding_db_from_text(text):
#     # CREATE EMBEDDINGS TO TEST SIMILARITY SCORES
#     return openai.embeddings.create(input = [text], model="text-embedding-ada-002").data[0].embedding



# def create_vector_db_from_text(text: str) -> FAISS:
#     # FAISS HELPS US DO THE SIMILARITY SEARCH
#     db = FAISS.from_texts([text], embeddings)
#     return db

# def get_response_from_query_about_textfiles(file_dbs, user_query, k_similarity=4):
#     # llm we chose, text-davinci, can handle 4097 tokens
#     # k_similarity = since each document chunk is 1000, we can search roughly 4 documents, so our k should be set to 4
#     # search the query relevant documents
#     # what did they say about X in the video
#     # the search will search only the document that is relevant to our query
#     files_texts = []
#     for file_db in file_dbs:    
#         file_text = file_db.similarity_search(user_query, k_similarity)
#         files_texts.append(file_text)


#     llm = OpenAI(model="gpt-3.5-turbo-instruct")

#     prompt = PromptTemplate(
#         input_variables = ["query","doc_one", "doc_two"],
#         template = gpt_template
#     )

#     chain = LLMChain(llm=llm, prompt=prompt)
#     response = chain.run(question=user_query, doc_one=files_texts[0], doc_two=files_texts[1])
#     # response = response.replace("\n", "")

#     return response