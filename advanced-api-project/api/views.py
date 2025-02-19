from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions

# Create your views here.
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # Admin users can perform any action
        return obj.author == request.user  # Only the author can update or delete their book

# List all books
class BookListView(generics.ListAPIView):
    """
    Allows users to filter, search, and order books based on different attributes.
    Available filters:
        - title
        - author
        - publication_year
    Available search fields:
        - title
        - author
    Available ordering:
        - title
        - publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['title', 'author', 'publication_year']  # Fields for filtering
    search_fields = ['title', 'author']  # Fields for searching
    ordering_fields = ['title', 'publication_year']  # Fields for ordering
    ordering = ['title']  # Default ordering by title

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        # You can add additional logic here, e.g., setting the author as the current user
        serializer.save(author=self.request.user)

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update
    permission_classes = [IsOwnerOrAdmin]

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
    permission_classes = [IsOwnerOrAdmin]

