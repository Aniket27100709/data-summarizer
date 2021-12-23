import streamlit as st
from transformers import pipeline

@st.cache(allow_output_mutation=True)
def summarizer():
    model = pipeline('summarization',device=0)
    return model
def chunks(text):
    max_chunk=1000
    text = text.replace('.','.<eos>')
    text = text.replace('?','?<eos>')
    text = text.replace('!','!<eos>')
    sentences=text.split('<eos>')
    curr=0
    chunk=[]
    for sentence in sentences:
        if len(chunk)==curr+1:
            if len(chunk[curr])+len(sentence.split(' '))<=max_chunk:
                chunk[curr].extend(sentence.split(' '))
            else:
                curr=0
                chunk.append(sentence.split(' '))
        else:
            chunk.append(sentence.split(' '))
    
    for i in range(len(chunk)):
        chunk[i]=' '.join(chunk[i])
    return chunk


summarize = summarizer()
st.title("Data Summarizer")
sentence = st.text_area('Enter the sentences', height=500)
button = st.button("Summarize")

max = st.sidebar.slider('Select max words', 100, 500, step=20, value=150)
min = st.sidebar.slider('Select min words', 10, 400, step=10, value=50)

with st.spinner("Generating Summary.."):
    if button and sentence:
        words = chunks(sentence)
        result = summarize(words,max_length=max,min_length=min)
        texts = ' '.join([summ['summary_text'] for summ in result])
        st.write(texts)