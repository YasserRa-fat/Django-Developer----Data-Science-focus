from django.urls import path
from .views import BookListView, BookDetailView, AuthorListView, AuthorDetailView, FavoriteListView, RegisterView,RecommendedBooksView,MyTokenObtainPairView,FavoriteDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<str:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/<int:pk>/', FavoriteDetailView.as_view(), name='favorite-detail'), 
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recommended/', RecommendedBooksView.as_view(), name='recommended-books'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
