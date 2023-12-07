import streamlit as st
from utils.crawl import crawl
from apis.func import chatgpt_func

st.set_page_config(layout="wide")

transalted_abstract = ''
translate_check = False

lang = chatgpt_func()

st.title('[Paper Searcher]')

search_text = st.text_input('')

st.sidebar.header('Hello this is Paper Searcher')
st.sidebar.write('crawl with arxiv')
st.sidebar.write('저자, 어디 퍼블리싱 되었나, 날짜')
st.sidebar.write('오른쪽에 북마크 왼쪽에 번역 같이 놓기, pdf 다운로드')
st.sidebar.write('년도, 최신순, 연관성, 저자이름, 퍼블리쉬 된곳만 보기')
search_size = st.sidebar.select_slider(
    'choose search size',
    options=[25, 50, 100, 200])
sort_type = st.sidebar.selectbox(
    'choose sort type',
    ('relevance', 'announcement date')
)
st.sidebar.write('\n\n\n\n made by acer')

if search_text != '':
    titles, urls, abstracts, dates, authors = crawl(search_text, search_size, sort_type)

col1, col2 = st.columns(2)

# if 'bookmark' not in st.session_state:
#     st.session_state['bookmark'] = []

# print(st.session_state['bookmark'])

st.session_state['bookmark'] = []

@st.cache_data
def book_mark_cache(data):
    return st.session_state['bookmark'].append(data)

with col1:
    count = 0
    for title, url, abstract, date, author in zip(titles, urls, abstracts, dates, authors):

        st.header(f'{title}\n')
        abstracted, _ = lang.preprocess(abstract)
        
        st.info(abstracted)
        st.info(date)
        st.info(', '.join(author))

        b1, b2, b3 = st.columns([1, 1, 1])
        translate_check = b1.button('translate', key = str(count))
        bookmark_check = b2.button('bookmark', key = str(count)+'|'+str(count))
        download_check = b3.button('download', key = str(count)+'|'+str(count)+'|'+str(count))
        if translate_check:
            with st.spinner('wait'):
                translated_title = title
                transalted_abstracted = lang.translate_func(abstracted)
            st.success(transalted_abstracted)

        if bookmark_check:
            st.session_state['bookmark'] = book_mark_cache(count)
            print(st.session_state['bookmark'])

        st.markdown('---')
        count += 1

with col2:
    print('here')
    st.header('Book Mark')
    # if lang.translate_func:
    #     print('here')
    #     st.header(translated_title)
    #     st.error(transalted_abstracted)