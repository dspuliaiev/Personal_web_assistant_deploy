from django.shortcuts import render
from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

def fetch_pravda_news(keyword):
    url = 'https://www.pravda.com.ua/rss/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        news = []
        for item in items:
            title = item.find('title')
            if title and (keyword is None or keyword.lower() in title.text.lower()):  # We check that the title exists and filter the news by keyword
                link = item.find('link').text
                description = item.find('description').text
                news.append({'title': title.text, 'link': link, 'description': description})
        return news
    else:
        print("Failed to fetch news from Pravda.com.ua RSS feed.")
        return []

def news_list(request):
    keyword = request.GET.get('keyword')
    if keyword:
        pravda_news = fetch_pravda_news(keyword)
    else:
        pravda_news = fetch_pravda_news('')  # We don't pass an argument to get all the news


    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(pravda_news, 10)  # Show 10 news per page
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