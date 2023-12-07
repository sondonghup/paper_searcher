import streamlit as st
from utils.crawl import crawl
from apis.func import chatgpt_func

st.set_page_config(layout="wide")

transalted_abstract = ''
translate_check = False

st.title('[Paper Searcher]')

st.sidebar.header('Hello this is Paper Searcher')
st.sidebar.write('crawl with arxiv')
st.sidebar.write('-----------------')
st.sidebar.write('저자, 어디 퍼블리싱 되었나, 날짜')
st.sidebar.write('오른쪽에 북마크 왼쪽에 번역 같이 놓기, pdf 다운로드')
st.sidebar.write('년도, 최신순, 연관성, 저자이름, 퍼블리쉬 된곳만 보기')
st.sidebar.write('-----------------')
open_ai_key = st.sidebar.text_input(
    'input your open ai key',
)
search_size = st.sidebar.select_slider(
    'choose search size',
    options=[25, 50, 100, 200])
sort_type = st.sidebar.selectbox(
    'choose sort type',
    ('relevance', 'announcement date')
)
st.sidebar.write('\n\n\n\n made by acer')

lang = chatgpt_func(open_ai_key)

search_text = st.text_input('')

if not search_text :
    st.write('please input')

if search_text != '':
    titles, urls, abstracts, dates, authors = crawl(search_text, search_size, sort_type)

# col1, col2 = st.columns(2)

st.session_state['bookmark'] = []

@st.cache_data
def book_mark_cache(data):
    return st.session_state['bookmark'].append(data)

count = 0
for title, url, abstract, date, author in zip(titles, urls, abstracts, dates, authors):

    tab1, tab2 = st.tabs(['abs', 'trans'])

    with tab1:
        st.header(f'{title}\n')
        abstracted, _ = lang.preprocess(abstract)
        
        st.info(abstracted)
        st.info(date)
        st.info(', '.join(author))

        b1, b2, b3 = st.columns([1, 1, 1])
        # translate_check = b1.button('translate', key = str(count))
        bookmark_check = b2.button('bookmark', key = str(count)+'|'+str(count))
        download_check = b3.button('download', key = str(count)+'|'+str(count)+'|'+str(count))

        st.markdown('---')

    with tab2:
        st.header(f'{title}\n')
        with st.spinner('wait'):
            translated_title = title
            transalted_abstracted = lang.translate_func(abstracted)
        st.success(transalted_abstracted)

        if bookmark_check:
            st.session_state['bookmark'] = book_mark_cache(count)
            print(st.session_state['bookmark'])

        st.markdown('---')
    count += 1

# with col2:
#     print('here')
#     st.header('Book Mark')
#     # if lang.translate_func:
#     #     print('here')
#     #     st.header(translated_title)
#     #     st.error(transalted_abstracted)
# except Exception as e:
# print(e)