import streamlit as st
from utils.crawl import crawl
from apis.func import chatgpt_func

st.set_page_config(layout="wide")

transalted_abstract = ''
translate_check = False

st.image('./paper_researcher_logo.png')

### side bar function ###
st.sidebar.image('./paper_researcher_logo_mini.png')
st.sidebar.title('Hello this is Paper Searcher')

tab1, tab2 = st.sidebar.tabs(['Info', 'Book Mark'])

with tab1:

    # st.sidebar.write('crawl with arxiv')
    # st.sidebar.write('저자, 어디 퍼블리싱 되었나, 날짜')
    # st.sidebar.write('오른쪽에 북마크 왼쪽에 번역 같이 놓기, pdf 다운로드')
    # st.sidebar.write('년도, 최신순, 연관성, 저자이름, 퍼블리쉬 된곳만 보기')

    st.write('Please enter open AI key for quick translation')
    st.write('If you do not input it, translation will take a lot of time.')
    
    st.write('-----------------')
    open_ai_key = st.text_input(
        '**input your open ai key**',
        type='password'
    )
    search_size = st.select_slider(
        '**choose search size**',
        options=[25, 50, 100, 200])
    sort_type = st.selectbox(
        '**choose sort type**',
        ('relevance', 'announcement date')
    )
    ##########################

with tab2:
    st.write('BOOK MARK')    

st.sidebar.write('-----------------')
st.sidebar.write('I would like to give you a lot of help in reading the paper.')
st.sidebar.write('The purpose is to summarize the abstract once more to quickly obtain the necessary information.')
st.sidebar.write('It also has additional features such as translation and downloading.')
st.sidebar.write('\n\n\n\n made by acer')

lang = chatgpt_func(open_ai_key)

search_text = st.text_input('')

if search_text != '':

    titles, urls, abstracts, dates, authors, file_urls = crawl(search_text, search_size, sort_type)

    st.session_state['bookmark'] = []

    @st.cache_data
    def book_mark_cache(data):
        return st.session_state['bookmark'].append(data)

    count = 0
    for title, url, abstract, date, author, file_url in zip(titles, urls, abstracts, dates, authors, file_urls):

        tab3, tab4 = st.tabs(['Abstract', 'Translate'])
        author = ', '.join(author).replace('Authors', '').replace(':', '')

        with tab3:
            st.header(f'{title}\n')
            st.markdown(f'<div style="text-align: right">{date}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: right">{author}</div>', unsafe_allow_html=True)

            # b1, b2, b3 = st.columns([1, 1, 1])
            # translate_check = b1.button('translate', key = str(count))
            # bookmark_check = b2.button('bookmark', key = str(count)+'|'+str(count))
            # download_check = b3.button('download', key = str(count)+'|'+str(count)+'|'+str(count))

            abstracted, _ = lang.preprocess(abstract)
            st.divider()
            st.markdown(abstracted)

            translate_check = st.toggle('Translate', key = str(count))
            bookmark_check = st.toggle('Bookmark', key = str(count)+'|'+str(count))
            # download_check = st.button('download', key = str(count)+'|'+str(count)+'|'+str(count))
            st.link_button('Download', file_url)


            st.markdown('---')

        with tab4:
            st.header(f'{title}\n')
            st.markdown(f'<div style="text-align: right">{date}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: right">{author}</div>', unsafe_allow_html=True)
            st.divider()

            if translate_check:
                with st.spinner('wait'):
                    translated_title = title
                    transalted_abstracted = lang.translate_func(abstracted)
                st.success(transalted_abstracted)

            if bookmark_check:
                st.session_state['bookmark'] = book_mark_cache(count)
                print(st.session_state['bookmark'])

            bookmark_check = st.toggle('bookmark', key = str(count + 1)+'|'+str(count + 1))
            # download_check = st.button('download', key = str(count + 1)+'|'+str(count + 1)+'|'+str(count + 1))
            st.link_button('Download', file_url)

            st.markdown('---')

        count += 2

    # with col2:
    #     print('here')
    #     st.header('Book Mark')
    #     # if lang.translate_func:
    #     #     print('here')
    #     #     st.header(translated_title)
    #     #     st.error(transalted_abstracted)
    # except Exception as e:
    # print(e)