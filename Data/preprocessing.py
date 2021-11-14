import re
import fitz
import pandas as pd

doc = fitz.open("FAQ_Shepell_workhealthlife.pdf")
n = doc.page_count
text = ""

# Collate the raw text from all pages of pdf
for pn in range(n):
    page = doc.loadPage(pn) #put here the page number
    text += page.getText()

text = re.sub(r'\n \n\d \n','',text)

questions = []
responses = []

for paragraph in text.split('\n \n'):
    ques = paragraph.split('\n')[0]
    res = paragraph.split('\n')[1:]
    res = ' '.join(res)
    
    ## Capture the sentences that starts with Question: pattern
    if 'Question:' in ques:
        questions.append(ques.replace('Question:','').strip())

    ## Capture the sentences that starts with Answer: pattern
    if 'Answer:' in res:
        responses.append(res.replace('Answer:','').strip())

# Putting data in pandas.DataFrame format
df = pd.DataFrame({'question':questions,'answer':responses})

## SOme clean up
df.fillna(value="", inplace=True)
df["question"] = df["question"].apply(lambda x: x.strip())
df.to_csv('FAQ_data.csv',index=False)