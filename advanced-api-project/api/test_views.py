from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book, Author

class BookTests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create an Author instance
        self.author = Author.objects.create(name="J.K. Rowling")

        # Create a Book instance and associate it with the Author instance
        self.book = Book.objects.create(
            title="Harry Potter",
            author=self.author,  # Use the Author instance
            publication_year=1997
        )
        self.client.login(username='testuser', password='testpassword')
    
    # Test GET all books
    def test_get_books(self):
        url = reverse('book-list')  # Assuming 'book-list' is the name of the endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure there is 1 book in the database

    # Test GET a single book
    def test_get_book(self):
        url = reverse('book-detail', args=[self.book.id])  # Assuming 'book-detail' is the name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')

    # Test POST create book
    def test_create_book(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'author': self.author.id,  # Ensure you're sending the author ID
            'publication_year': 2022
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Ensure a new book is created

    # Test PUT update book
    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])  # Assuming 'book-update' is the name
        data = {'title': 'Updated Title', 'author': 'J.K. Rowling', 'publication_year': 1998}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()  # Refresh from the database to check changes
        self.assertEqual(self.book.title, 'Updated Title')

    # Test DELETE book
    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])  # Assuming 'book-delete' is the name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Ensure the book is deleted

    # Test filtering books by title
    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Harry'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure only one book matches the title

    # Test searching books by author
    def test_search_books_by_author(self):
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test ordering books by title
    def test_ordering_books_by_title(self):
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test the order by title
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    # Test permissions (non-authenticated user should not create or delete books)
    def test_permission_for_create_book(self):
        self.client.logout()  # Logout the authenticated user
        url = reverse('book-create')
        data = {'title': 'Unauthorized Book', 'author': 'Unknown', 'publication_year': 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)