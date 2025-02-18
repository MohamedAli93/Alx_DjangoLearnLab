from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList

# Create a router instance
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')  # Registers the ViewSet

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # ListAPIView route
    path('', include(router.urls)),  # Includes all router-generated URLs
]