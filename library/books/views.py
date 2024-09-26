from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author, Favorite
from .serializers import BookSerializer, AuthorSerializer, FavoriteSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from rest_framework_simplejwt.views import TokenObtainPairView

# Set up logging
logger = logging.getLogger(__name__)

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'authors__name']

    def perform_create(self, serializer):
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class FavoriteListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        # Check if the book is already in the user's favorites
        book_id = self.request.data.get('book')  # Assuming 'book' is the field for the book ID
        user = self.request.user
        # Check if the user already has 20 favorites
        if Favorite.objects.filter(user=self.request.user).count() >= 20:
            raise serializers.ValidationError("You can only have a maximum of 20 favorite books.")
        
        if Favorite.objects.filter(user=user, book_id=book_id).exists():
            raise serializers.ValidationError("This book is already in your favorites.")

        # Save the new favorite
        favorite = serializer.save(user=user)

        # Get the recommendations based on the user's favorites
        recommended_books = self.get_recommendations()

        # Add the newly added favorite for use in the response
        self.added_favorite = favorite.book

    def get_recommendations(self):
        # Get the user's favorite books
        favorites = Favorite.objects.filter(user=self.request.user)
        favorite_books = [fav.book for fav in favorites]

        if not favorite_books:
            return []  # Return empty if no favorites

        # Extract authors from favorite books
        favorite_authors = [author for book in favorite_books for author in book.authors.all()]

        # Find books by those authors but exclude the books already in favorites
        similar_books = Book.objects.filter(authors__in=favorite_authors).exclude(id__in=[book.id for book in favorite_books])

        # Limit to 5 recommendations
        recommended_books = similar_books.distinct()[:5]

        return recommended_books

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Get the added favorite book and recommendations
        added_favorite = self.added_favorite
        recommended_books = self.get_recommendations()

        # Get only the titles for the added favorite book and recommended books
        added_favorite_title = added_favorite.title if added_favorite else None
        recommended_book_titles = [book.title for book in recommended_books]

        # Include only the titles in the response
        response.data['added_favorite'] = added_favorite_title
        response.data['recommended_books'] = recommended_book_titles

        return response



class FavoriteDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Favorite.objects.all()
    
    def get_object(self):
        # Get the favorite instance for the current user
        favorite = super().get_object()
        if favorite.user != self.request.user:
            self.permission_denied(self.request)
        return favorite


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)

class RecommendedBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Fetch the user's favorite books
        favorites = Favorite.objects.filter(user=user).select_related('book')
        favorite_books = [favorite.book for favorite in favorites]

        if not favorite_books:
            return Response([])  # Return empty if no favorites

        # Get features for all books in the database
        all_books = Book.objects.all()
        book_titles = [book.title for book in all_books]
        book_ids = [book.id for book in all_books]

        # Prepare a matrix of features (e.g., average_rating, num_pages, etc.)
        features = []
        for book in all_books:
            features.append([
                book.average_rating,  # Example feature
                book.num_pages,  # Example feature
                # Add other relevant features as needed
            ])
        
        features = np.array(features)

        # Get features for favorite books
        favorite_features = []
        for book in favorite_books:
            index = book_ids.index(book.id)
            favorite_features.append(features[index])
        
        # Compute the mean feature vector for the favorite books
        mean_favorites = np.mean(favorite_features, axis=0).reshape(1, -1)

        # Calculate cosine similarity between the mean favorites and all books
        similarities = cosine_similarity(mean_favorites, features).flatten()

        # Get the indices of the top 5 recommended books (excluding the favorite books)
        recommended_indices = similarities.argsort()[-6:-1]  # Exclude the favorite book itself

        # Extract only the titles of the recommended books
        recommended_books = [book_titles[i] for i in recommended_indices]
        
        # Return the titles of the recommended books
        return Response(recommended_books)



class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
