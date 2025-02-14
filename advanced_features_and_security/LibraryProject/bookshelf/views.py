from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book

# Create your views here.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST["title"]
        author = request.POST["author"]
        published_date = request.POST["published_date"]
        book = Book.objects.create(title=title, author=author, published_date=published_date, created_by=request.user)
        return redirect('book_list')
    return render(request, 'books/book_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST["title"]
        book.author = request.POST["author"]
        book.published_date = request.POST["published_date"]
        book.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')