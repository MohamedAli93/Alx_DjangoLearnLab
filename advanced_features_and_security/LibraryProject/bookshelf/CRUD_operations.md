book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Successfully created a new book object. No output is displayed for successful creation.
all_books = Book.objects.all()
book = all_books.first()
# Output: 
# <Book: 1984 by George Orwell> (This will display details of the created book)
book.title = "Nineteen Eighty-Four"
book.save()
# No output displayed for successful update. You can verify by retrieving the book again.
book.delete()
all_books = Book.objects.all()
# No books found. Output: QuerySet[<Book>] (empty)