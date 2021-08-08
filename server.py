from fastapi import FastAPI
from haystack import Finder
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.dense import EmbeddingRetriever
from haystack.utils import print_answers
from haystack.pipeline import FAQPipeline
import pandas as pd

app = FastAPI()

store = None
retr = None
pipe = None

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
    store = _document_store()
    retr = _document_retriever(document_store=document_store, embedding_model="sentence-transformers/paraphrase-albert-small-v2")
    pipeline = _faq_pipeline(retriever=retr)

    df = pd.read_csv('FAQ/FAQ_Shepell_workhealthlife.pdf')
    questions = list(df["question"].values)
    df["question_emb"] = retriever.embed_queries(texts=questions)
    df = df.rename(columns={"question": "text"})
    
    docs_to_index = df.to_dict(orient="records")
    store.write_documents(docs_to_index)

@app.post('/search')
def search(query:str):
    prediction = pipe.run(query=query, top_k_retriever=1)
    prediction = prediction['answers'][0]['answer']
    return {'answer':prediction}
    