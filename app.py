from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from src.helper import load_pdf, text_split
import os
from langchain_community.llms import OpenAI
from langchain_objectbox.vectorstores import ObjectBox ##vector Database

load_dotenv()

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



os.environ["OPENAI_API_KEY"]=""



embedding=OpenAIEmbeddings()

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)



vectors = ObjectBox.from_documents(text_chunks, OpenAIEmbeddings(), embedding_dimensions=768)
PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}








llm=OpenAI()

qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                  chain_type="stuff",
                                 retriever=vectors.as_retriever(),
                                  return_source_documents=True,
                                  chain_type_kwargs=chain_type_kwargs)


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


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/get", response_class=HTMLResponse)
async def chat(msg: str = Form(...)):
    input = msg
    result = qa_chain({"query": input})
    return result["result"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)