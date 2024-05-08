from django.urls import path
from news_scraping import views

app_name = 'news_scraping'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('news', views.news_list, name='news_list'),
]