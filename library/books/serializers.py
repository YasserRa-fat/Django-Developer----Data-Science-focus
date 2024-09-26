from rest_framework import serializers
from .models import Book, Author, Favorite
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'gender',
            'image_url',
            'about',
            'ratings_count',
            'average_rating',
            'text_reviews_count',
            'works_count',
            'fans_count',
            'work_ids',
            'book_ids'
        ]

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'authors',
            'author_name',
            'author_id',
            'work_id',
            'isbn',
            'isbn13',
            'asin',
            'language',
            'average_rating',
            'rating_dist',
            'ratings_count',
            'text_reviews_count',
            'publication_date',
            'original_publication_date',
            'format',
            'edition_information',
            'image_url',
            'publisher',
            'num_pages',
            'series_id',
            'series_name',
            'series_position',
            'description'
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['book']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
