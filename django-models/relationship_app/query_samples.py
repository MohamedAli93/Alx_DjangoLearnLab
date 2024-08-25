import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        return [book.title for book in books]
    except Author.DoesNotExist:
        return None


# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return [book.title for book in books]
    except Library.DoesNotExist:
        return None


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian.name
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None


# Example usage
if __name__ == "__main__":
    print(get_books_by_author("Author Name"))
    print(get_books_in_library("Library Name"))
    print(get_librarian_for_library("Library Name"))