import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assistant_project.settings")
django.setup()

from notes.models import Tag

# Очистка всех существующих тегов
Tag.objects.all().delete()

# Список тегов, которые будут добавлены
tags = [
    "Work", "Study", "Home", "Travel", "Health",
    "Sports", "Technology", "Art", "Music", "Cooking",
    "Personal Development", "Finance", "Relationships", "Holidays", "Books",
    "Movies", "Games", "Shopping", "Repairs", "Events",
    "Projects", "Mistakes", "Education", "Career", "Planning",
    "Nature", "Animals", "Self Care", "Ecology", "Science"
]

# Добавление новых тегов в базу данных
for tag_name in tags:
    Tag.objects.get_or_create(name=tag_name)
