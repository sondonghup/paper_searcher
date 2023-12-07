import requests
from bs4 import BeautifulSoup as bs
import re

def crawl(search_text, search_size, sort_type):
    titles = []
    urls = []
    abstracts = []
    authors = []
    dates = []
    file_urls = []

    if sort_type == 'newest' :
        sort_type = '-announced_date_first'
    elif sort_type == 'oldest' :
        sort_type = 'announced_date_first'
    elif sort_type == 'relevance':
        sort_type = ''

    url = f'https://arxiv.org/search/cs?query={search_text}&searchtype=all&abstracts=show&order={sort_type}&size={search_size}'

    response = requests.get(url)
    html = bs(response.text, 'html.parser')
    thesis_tables = html.find('div', {'class' : 'content'})
    # print(thesis_tables)
    thesis_table = thesis_tables.find_all('li', {'class' : 'arxiv-result'})
    for line in thesis_table:

        file_url = line.find('p', {'class' : 'list-title is-inline-block'})
        file_url = file_url.find('span').find_all('a')
        file_urls.append(file_url[0]['href'])

        author = line.find('p', {'class' : 'authors'}).text.replace('\n', '').split(',')
        author = [x.strip() for x in author][:3]
        authors.append(author)

        title = line.find('p', {'class' : 'title is-5 mathjax'}).text
        titles.append(title)

        url = line.find('p', {'class' : 'list-title is-inline-block'}).find('a')['href']
        urls.append(url)

        date = line.find('p', {'class' : 'is-size-7'}).text.split(';')[0]
        dates.append(date)

        abstract = line.find('span', {'class' : "abstract-full has-text-grey-dark mathjax"}).text.split('△ Less')[0].strip()
        # abstract = preprocess(abstract)
        abstracts.append(abstract)

    return titles, urls, abstracts, dates, authors, file_urls

def preprocess(abstract):
    return re.sub("[^A-Za-z0-9가-힣]",' ',abstract)

if __name__ == '__main__':
    crawl('sbert')
