from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import ExampleForm
from django.db.models import Q

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

def book_list(request):
    books = Book.objects.all()  # Fetch all books
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_search(request):
    query = request.GET.get('search', '')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    
    return render(request, 'bookshelf/book_list.html', {'books': books})

def add_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # ✅ Redirect to a book listing page
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})