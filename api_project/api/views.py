from rest_framework import generics  # Ensure this import is present
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):  # Ensure this extends generics.ListAPIView
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):  # Extends ModelViewSet to handle CRUD
    queryset = Book.objects.all()
    serializer_class = BookSerializer