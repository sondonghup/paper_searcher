import streamlit as st
from utils.crawl import crawl
import requests
st.set_page_config(layout="wide")

st.title('Paper Searcher')


search_text = st.text_input('')
titles, urls, abstracts = crawl(search_text)

col1, col2 = st.columns(2)

transalted_abstract = ''
translate_check = False

def translate(input_text):
    url = "http://localhost:9001/translate"
    data = {"text": input_text}
    response = requests.post(url, json=data)
    return response.json()['Translating']


with col1:
    count = 0
    for title, url, abstract in zip(titles, urls, abstracts):

        st.write(f'{title}\n')
        st.info(abstract)
        translate_check = st.checkbox('translate', key = count)
        if translate_check:
            st.write('wait')
            translated_title = title
            transalted_abstract = translate(abstract)

        st.markdown('---')
        count += 1

with col2:

    if translate:
        st.write(translated_title)
        st.error(transalted_abstract)



    pass
        # st.markdown(html_str, unsafe_allow_html=True)
        # st.markdown('## :red[{temp1}]'.format(temp1=title))
        # st.markdown(title_html, unsafe_allow_html=True)
        # st.markdown(f'### {title}')
    


