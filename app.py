import streamlit as st
from utils.crawl import crawl

st.title('Thesis Searcher')

search_text = st.text_input('')
titles, urls, abstracts = crawl(search_text) 

for title, url, abstract in zip(titles, urls, abstracts):
    # st.markdown(':red[fksdnsekls]')
    st.markdown(f':red[{title}]')
    st.markdown('---')


