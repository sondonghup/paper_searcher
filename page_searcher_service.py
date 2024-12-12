import streamlit as st
from utils.crawl import crawl
from apis.func import chatgpt_func
import datetime

st.set_page_config(layout="wide")

st.image('./paper_searcher_logo.png')

if 'bookmarks' not in st.session_state:
    st.session_state['bookmarks'] = []
if 'bookmarknum' not in st.session_state:
    st.session_state['bookmarknum'] = 0
if 'translatedcheck' not in st.session_state:
    st.session_state['translatedcheck'] = []
if 'alreadysearch' not in st.session_state:
    st.session_state['alreadysearch'] = 0
if 'titles' not in st.session_state:
    st.session_state['titles'] = []
if 'urls' not in st.session_state:
    st.session_state['urls'] = []
if 'abstracts' not in st.session_state:
    st.session_state['abstracts'] = []
if 'dates' not in st.session_state:
    st.session_state['dates'] = []
if 'authors' not in st.session_state:
    st.session_state['authors'] = []
if 'file_urls' not in st.session_state:
    st.session_state['file_urls'] = []
if 'search_text' not in st.session_state:
    st.session_state['search_text'] = []
if 'search_count' not in st.session_state:
    st.session_state['search_count'] = 0
if 'bookmarkcheck' not in st.session_state:
    st.session_state['bookmarkcheck'] = []

### side bar function ###
st.sidebar.image('./paper_searcher_logo_mini.png')
st.sidebar.title(' :wave: Hello this is Paper Searcher')

tab1, tab2 = st.sidebar.tabs(['Settings', 'Book Mark'])

with tab1:

    # st.sidebar.write('crawl with arxiv')
    # st.sidebar.write('저자, 어디 퍼블리싱 되었나, 날짜')
    # st.sidebar.write('오른쪽에 북마크 왼쪽에 번역 같이 놓기, pdf 다운로드')
    # st.sidebar.write('년도, 최신순, 연관성, 저자이름, 퍼블리쉬 된곳만 보기')
    # 하이라이트 해주기

    st.divider()
    open_ai_key = st.text_input(
        ' :heavy_check_mark: **input your open ai key**',
        type='password'
    )
    # st.write('Please enter open AI key for quick translation')
    
    st.divider()
    search_size = st.select_slider(
        ' :heavy_check_mark: **choose search size**',
        options=[25, 50, 100, 200])
    # st.write('Enter number per page 25, 50, 100, 200')
    
    st.divider()
    search_term = st.selectbox(
        ' :heavy_check_mark: **choose search term**',
        ('title', 'author', 'abstract')
    )

    st.divider()
    sort_type = st.selectbox(
        ' :heavy_check_mark: **choose sort type**',
        ('relevance', 'newest', 'oldest')
    )

    st.divider()
    from_date = st.date_input(
        'from_date',
        value = datetime.date(2020, 1, 1),
        min_value = datetime.date(2000, 1, 1)
    )

    st.divider()
    to_date = st.date_input(
        'to_date',
        min_value = datetime.date(2000, 1, 1)
    )
    # st.write('Enter sort type')
    ##########################

with tab2:
    st.write('BOOK MARK')

st.sidebar.write('-----------------')
st.sidebar.write('I would like to give you a lot of help in reading the paper.')
st.sidebar.write('The purpose is to summarize the abstract once more to quickly obtain the necessary information.')
st.sidebar.write('It also has additional features such as translation, bookmarking and downloading.')
st.sidebar.write('\n\n\n\n made by acer')

lang = chatgpt_func(open_ai_key)



search_text = st.text_input(':dark_sunglasses: What topic would you like to find a paper on?')

if not search_text:
    st.header(':arrow_down: GUIDE!! :arrow_down:')
    st.video('./paper_searcher_guide.webm')

if len(st.session_state['search_text']) > 1 and search_text != st.session_state['search_text'][-1]:
    st.session_state['titles'] = []
    st.session_state['urls'] = []
    st.session_state['abstracts'] = []
    st.session_state['dates'] = []
    st.session_state['authors'] = []
    st.session_state['file_urls'] = []
    st.session_state['search_text'] = []
    st.session_state['alreadysearch'] = 0
    st.session_state['search_count'] += 1
    st.session_state['bookmarkcheck'] = []
    st.session_state['translatedcheck'] = []

st.session_state['search_text'].append(search_text)

if search_text != '':

    count = 0

    if st.session_state['alreadysearch'] == 0:
        st.session_state['titles'], st.session_state['urls'], st.session_state['abstracts'], st.session_state['dates'], st.session_state['authors'], st.session_state['file_urls'] = crawl(search_text, search_size, sort_type, from_date, to_date, search_term)

    for title, url, abstract, date, author, file_url in zip(st.session_state['titles'], st.session_state['urls'], st.session_state['abstracts'], st.session_state['dates'], st.session_state['authors'], st.session_state['file_urls']):

        tab3, tab4 = st.tabs(['Abstract', 'Translate'])
        author = ', '.join(author).replace('Authors', '').replace(':', '')

        with tab3:
            st.header(f'{title}\n')
            st.markdown(f'<div style="text-align: right">{date}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: right">{author}</div>', unsafe_allow_html=True)

            abstracted, _ = lang.preprocess(abstract)
            st.divider()
            st.success(abstracted)

            translate_check = st.toggle('Translate', key = str(count) + '|'+ str(st.session_state['search_count']))
            bookmark_check = st.toggle('Bookmark', key = str(count)+'|'+str(count)+ '|' + str(st.session_state['search_count']))

            st.link_button('Download', file_url)
            st.markdown('---')

        with tab4:
            st.header(f'{title}\n')
            st.markdown(f'<div style="text-align: right">{date}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: right">{author}</div>', unsafe_allow_html=True)
            st.divider()

            try:
                if translate_check and count not in st.session_state['translatedcheck']:
                    st.session_state['translatedcheck'].append(count)
                    print('번역 숫자', st.session_state['translatedcheck'])
                    with st.spinner('wait'):
                        translated_title = title
                        transalted_abstracted = lang.translate_func(abstracted)
                    st.success(transalted_abstracted)
            except Exception as e:
                print(e)
                pass

            st.link_button('Download', file_url)

            if bookmark_check and count not in st.session_state['bookmarkcheck']:
                st.session_state['bookmarkcheck'].append(count)
                st.session_state['bookmarks'].append([title, file_url])

            st.markdown('---')

        count += 1
        st.session_state['alreadysearch'] += 1

with tab2:
    if st.session_state['bookmarks'] == []:
        pass
    else :
        st.session_state['bookmarknum'] += 1
        for (title, file) in st.session_state['bookmarks'][-1 * st.session_state['bookmarknum'] : ]:
            st.divider()
            st.error(title)
            st.link_button('Download', file_url)
