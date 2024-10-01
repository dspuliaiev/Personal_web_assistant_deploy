from django.contrib import admin
from django.urls import path, include
from contacts.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('contacts/', include('contacts.urls')),
    path('users/', include('users.urls')),
    path('notes/', include('notes.urls')),
    path('files/', include('files.urls')),
    path('weather/', include('weather.urls')),
    path('news/', include('news_scraping.urls')),
]
