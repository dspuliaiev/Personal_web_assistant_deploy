import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from html import unescape
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def fetch_news(keyword, urls):
    news = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            for item in items:
                title = item.find('title')
                if title and (keyword is None or keyword.lower() in title.text.lower()):
                    link = item.find('link').text
                    description = item.find('description').text
                    if description:
                        description = strip_tags(description)
                        description = unescape(description)
                    news.append({'title': title.text, 'link': link, 'description': description})
        else:
            print(f"Failed to fetch news from {url} RSS feed.")
    return news

def news_list(request):
    keyword = request.GET.get('keyword')
    urls = [
        'https://www.pravda.com.ua/rss/',
        'https://bin.ua/news/rss.xml',
        'https://rbc.ua/static/rss/all.ukr.rss.xml',
        'https://inform-ua.info/feed/rss/v1'
    ]
    if keyword:
        all_news = fetch_news(keyword, urls)
    else:
        all_news = fetch_news(None, urls)

    # Pagination
    paginator = Paginator(all_news, 10)  # Show 10 news per page
    page = request.GET.get('page')
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, output the first page
        news_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, print last page
        news_list = paginator.page(paginator.num_pages)

    context = {
        'news_list': news_list,
        'keyword': keyword
    }

    return render(request, 'news/news_list.html', context)