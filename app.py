import streamlit as st
from utils.crawl import crawl
# from apis.func import lang_chain
from apis.func import chatgpt_func

st.set_page_config(layout="wide")
# @st.cache_resource()
# def load_chain():
#     return lang_chain()

lang = chatgpt_func()

st.title('[Paper Searcher]')

search_text = st.text_input('')
titles, urls, abstracts = crawl(search_text)

col1, col2 = st.columns(2)

transalted_abstract = ''
translate_check = False

with col1:
    count = 0
    for title, url, abstract in zip(titles, urls, abstracts):

        st.write(f'{title}\n')
        # abstract = abstract.split('')
        abstracted = lang.preprocess(abstracts)
        
        st.info(abstracted)
        translate_check = st.checkbox('translate', key = count)
        if translate_check:
            st.write('wait')
            translated_title = title
            transalted_abstracted = lang.translate_func(abstracted)
            print(transalted_abstracted)

        st.markdown('---')
        count += 1

with col2:
    print('here')
    if lang.translate_func:
        print('here')
        st.write(translated_title)
        st.error(transalted_abstracted)
