import requests
from bs4 import BeautifulSoup as bs
import re

def crawl(search_text):
    titles = []
    urls = []
    abstracts = []

    url = f'https://arxiv.org/search/cs?query={search_text}&searchtype=all&abstracts=show&order=-announced_date_first&size=50'

    response = requests.get(url)
    html = bs(response.text, 'html.parser')
    thesis_tables = html.find('div', {'class' : 'content'})
    thesis_table = thesis_tables.find_all('li', {'class' : 'arxiv-result'})
    for line in thesis_table:
        title = line.find('p', {'class' : 'title is-5 mathjax'}).text
        titles.append(title)
        url = line.find('p', {'class' : 'list-title is-inline-block'}).find('a')['href']
        urls.append(url)
        abstract = line.find('span', {'class' : "abstract-full has-text-grey-dark mathjax"}).text.split('△ Less')[0].strip()
        abstract = preprocess(abstract)
        abstracts.append(abstract)

    return titles, urls, abstracts

def preprocess(abstract):
    return re.sub("[^A-Za-z0-9가-힣]",' ',abstract)

if __name__ == '__main__':
    crawl('sbert')
