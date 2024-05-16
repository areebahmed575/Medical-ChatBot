from flask import Flask, render_template, jsonify, request
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from src.helper import load_pdf, text_split
from store_index import vectordb
from src.helper import load_pdf, text_split
import os
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn


app = Flask(__name__)

load_dotenv()


os.environ["OPENAI_API_KEY"]=""



embedding=OpenAIEmbeddings()

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)

persist_directory = 'db'
vectordb = Chroma.from_documents(documents=text_chunks,embedding=embedding,persist_directory=persist_directory)
vectordb.persist() # persiste the db to disk
vectordb = None
# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,embedding_function=embedding)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}


retriever = vectordb.as_retriever(search_kwargs={"k": 2})





llm=OpenAI()

qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                  chain_type="stuff",
                                  retriever=retriever,
                                  return_source_documents=True)


## Cite sources
def process_llm_response(llm_response):
    print(llm_response['result'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])

# full example
query = "What are Allergies?"


llm_response = qa_chain.invoke(query)


print(llm_response)

print(process_llm_response(llm_response))




@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)