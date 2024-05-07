from django.urls import path
from .views import (
    category_create,
    categories,
    category_delete,
    files,
    files_id,
    create,
    download
)

app_name = 'files'

urlpatterns = [
    path('categories/', categories, name='categories'),
    path('category_create/', category_create, name='category_create'),
    path('category_delete/<int:category_id>', category_delete, name='category_delete'),
    path('', files, name='files'),
    path('files_id/<int:category_id>', files_id, name='files_id'),
    path('create', create, name='create'),
    path('download/<int:file_id>', download, name='download'),
]