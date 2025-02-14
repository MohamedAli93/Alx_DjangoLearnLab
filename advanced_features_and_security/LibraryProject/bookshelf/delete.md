from bookshelf.models import Book
book.delete()
all_books = Book.objects.all()
# No books found. Output: QuerySet[<Book>] (empty)