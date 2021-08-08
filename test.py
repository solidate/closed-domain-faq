from haystack import Finder
# from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.document_store.memory import InMemoryDocumentStore
# document_store = InMemoryDocumentStore()

from haystack.retriever.dense import EmbeddingRetriever
from haystack.utils import print_answers
import pandas as pd
import requests

from haystack.document_store.memory import InMemoryDocumentStore
document_store = InMemoryDocumentStore(similarity="cosine",index="document",
                                            embedding_field="question_emb",
                                            embedding_dim=768)


retriever = EmbeddingRetriever(document_store=document_store, embedding_model="sentence-transformers/paraphrase-albert-small-v2")

import fitz
doc = fitz.open("FAQ/FAQ_Shepell_workhealthlife.pdf")
n = doc.page_count
text = ""
for pn in range(n):
    page = doc.loadPage(pn) #put here the page number
    text += page.getText()

print(text.encode('utf-8'))

import re
text = re.sub(r'\n \n\d \n','',text)

questions = []
responses = []
context = []
start = []
begin = 0
for paragraph in text.split('\n \n'):
    ques = paragraph.split('\n')[0]
    res = paragraph.split('\n')[1:]
    res = ' '.join(res)
    context.append(res.replace('Answer:','').lstrip())
    begin += len(context[-1])
    print(len(context[-1]))

    if 'Question:' in ques:
        questions.append(ques.replace('Question:','').strip())

    if 'Answer:' in res:
        responses.append(res.replace('Answer:','').strip())
        start.append(begin-len(context[-1]))

df = pd.DataFrame({'question':questions,'answer':responses})

# # Download
# temp = requests.get("https://raw.githubusercontent.com/deepset-ai/COVID-QA/master/data/faqs/faq_covidbert.csv")
# open('small_faq_covid.csv', 'wb').write(temp.content)

# # Get dataframe with columns "question", "answer" and some custom metadata
# df = pd.read_csv("small_faq_covid.csv")
# Minimal cleaning
df.fillna(value="", inplace=True)
df["question"] = df["question"].apply(lambda x: x.strip())
print(df.head())

# Get embeddings for our questions from the FAQs
questions = list(df["question"].values)
df["question_emb"] = retriever.embed_queries(texts=questions)
# df["question_emb"] = retriever.eval()
df = df.rename(columns={"question": "text"})

# Convert Dataframe to list of dicts and index them in our DocumentStore
docs_to_index = df.to_dict(orient="records")
document_store.write_documents(docs_to_index)

print('**********','\n',docs_to_index,'*********')

from haystack.pipeline import FAQPipeline
pipe = FAQPipeline(retriever=retriever)

prediction = pipe.run(query="What to do in case of crisis?	", top_k_retriever=1)
print_answers(prediction, details="all")

