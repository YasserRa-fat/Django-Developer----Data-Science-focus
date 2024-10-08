# Generated by Django 5.1.1 on 2024-09-25 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=255)),
                ('author_id', models.CharField(max_length=255)),
                ('work_id', models.CharField(max_length=255)),
                ('isbn', models.CharField(max_length=20, unique=True)),
                ('isbn13', models.CharField(max_length=20, unique=True)),
                ('asin', models.CharField(blank=True, max_length=20, null=True)),
                ('language', models.CharField(max_length=10)),
                ('average_rating', models.FloatField()),
                ('rating_dist', models.TextField()),
                ('ratings_count', models.IntegerField()),
                ('text_reviews_count', models.IntegerField()),
                ('publication_date', models.DateField()),
                ('original_publication_date', models.DateField()),
                ('format', models.CharField(max_length=50)),
                ('edition_information', models.CharField(max_length=255)),
                ('image_url', models.URLField()),
                ('publisher', models.CharField(max_length=255)),
                ('num_pages', models.IntegerField()),
                ('series_id', models.CharField(max_length=255)),
                ('series_name', models.CharField(max_length=255)),
                ('series_position', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('authors', models.ManyToManyField(related_name='books', to='books.author')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
