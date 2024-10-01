from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.core.cache import cache
from .utils import fetch_news, strip_tags


def news_list(request):
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')

    # Используем ключ кэша, который включает ключевое слово
    cache_key = f'news_list_{keyword}'

    # Попытка получить данные из кэша
    all_news = cache.get(cache_key)

    if all_news is None:
        # Если данных нет в кэше, получаем их и сохраняем в кэш
        urls = [
            'https://www.pravda.com.ua/rss/',
            'https://bin.ua/news/rss.xml',
            'https://rbc.ua/static/rss/all.ukr.rss.xml',
            'https://inform-ua.info/feed/rss/v1'
        ]
        all_news = fetch_news(keyword, urls)

        # Кэшируем данные на 15 минут
        cache.set(cache_key, all_news, 60 * 15)

    # Пагинация
    paginator = Paginator(all_news, 10)  # Показывать 10 новостей на странице

    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    context = {
        'news_list': news_list,
        'keyword': keyword
    }

    return render(request, 'news/news_list.html', context)