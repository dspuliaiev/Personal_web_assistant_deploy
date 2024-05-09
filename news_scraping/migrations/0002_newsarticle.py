# Generated by Django 5.0.4 on 2024-05-07 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('source', models.CharField(max_length=100)),
                ('published_at', models.DateTimeField()),
            ],
        ),
    ]
