from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.dense import EmbeddingRetriever
from haystack.utils import print_answers
from haystack.pipeline import FAQPipeline
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./static/")
global store,retr,pipe


class Item(BaseModel):
    query : str

def _document_store(similarity="cosine",index="document",
                                            embedding_field="question_emb",
                                            embedding_dim=768):
    document_store = InMemoryDocumentStore(similarity=similarity,index=index,
                                            embedding_field=embedding_field,
                                            embedding_dim=embedding_dim)
    
    return document_store

def _document_retriever(document_store=None,embedding_model=None):
    retriever = EmbeddingRetriever(document_store=document_store, 
                                    embedding_model=embedding_model)

    return retriever

def _faq_pipeline(retriever=None):
    pipeline = FAQPipeline(retriever=retriever)

    return pipeline

@app.on_event("startup")
def startup_event():
    global store,retr,pipe
    store = _document_store()
    retr = _document_retriever(document_store=store, embedding_model="sentence-transformers/paraphrase-albert-small-v2")
    pipe =  _faq_pipeline(retriever=retr)

    df = pd.read_csv('Data/faq.csv')
    questions = list(df["question"].values)
    df["question_emb"] = retr.embed_queries(texts=questions)
    df = df.rename(columns={"question": "text"})
    
    docs_to_index = df.to_dict(orient="records")
    store.write_documents(docs_to_index)

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

    # return 'Go to /docs'

@app.post('/search/')
def search(item: Item):
    item = item.dict()
    query = item['query']
    global pipe
    prediction = pipe.run(query=query, params={"Retriever": {"top_k": 10}})
    prediction = prediction['answers'][0]['answer']
    return {'answer':prediction}
    