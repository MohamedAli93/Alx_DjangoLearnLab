from rest_framework import generics  # Ensure this import is present
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):  # Ensure this extends generics.ListAPIView
    queryset = Book.objects.all()
    serializer_class = BookSerializer