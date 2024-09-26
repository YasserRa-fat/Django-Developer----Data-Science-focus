from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)
    works_count = models.IntegerField(default=0)
    fans_count = models.IntegerField(default=0)
    work_ids = models.JSONField(default=list)
    book_ids = models.JSONField(default=list)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    author_name = models.CharField(max_length=255)
    author_id = models.CharField(max_length=255)
    work_id = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    isbn13 = models.CharField(max_length=20, unique=True)
    asin = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=10)
    average_rating = models.FloatField()
    rating_dist = models.TextField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.DateField()
    original_publication_date = models.DateField()
    format = models.CharField(max_length=50)
    edition_information = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200)
    publisher = models.CharField(max_length=255)
    num_pages = models.IntegerField()
    series_id = models.CharField(max_length=255)
    series_name = models.CharField(max_length=255)
    series_position = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
