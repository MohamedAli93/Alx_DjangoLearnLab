from django.shortcuts import render
from .models import Book  # Assuming you have a Book model in your app

def list_books(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.views.generic import DetailView
from .models import Library  # Assuming you have a Library model in your app

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    # Optionally override get_context_data if you need to add more data to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context