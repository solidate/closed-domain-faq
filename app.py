import requests
import json
import streamlit as st

def get_answer(query:str):
    response = requests.post('http://0.0.0.0:8000/search',json={'query':query})
    response = response.json()
    return response['answer']

def main():
    st.title("Closed domain FAQ System Demo")
    st.text('Please enter your query')
    user_input = st.text_area("Search box")
    output = get_answer(user_input)
    st.write(output)

if __name__=="__main__":
    main()