from src.helper import load_pdf, text_split
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
from langchain import embeddings

load_dotenv()


os.environ["OPENAI_API_KEY"]=""

embedding=OpenAIEmbeddings()
extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)




persist_directory = 'db'
vectordb = Chroma.from_documents(documents=text_chunks,embedding=embedding,persist_directory=persist_directory)
# vectordb.persist() # persiste the db to disk
# vectordb = None
# # Now we can load the persisted database from disk, and use it as normal.
# vectordb = Chroma(persist_directory=persist_directory,embedding_function=embedding)