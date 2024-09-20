from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework import status
from unittest import mock
from unittest.mock import patch
from .models import Category, Book, User, BorrowedBookLog
from .views import AddBookAPIView, BookNotAvailableListAPIView, DeleteBookAPIView, ListUsersAPIView
from api.publisher import publish_save_book_event
import pytest
from datetime import date, timedelta
   
        
@pytest.fixture
def request_factory():
    return APIRequestFactory()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def bad_data():
    return {
        'title': '',
        'author': '',
        'publisher': '',
        'category': ''
    }

# Create your tests here.

@pytest.mark.django_db
def test_add_book_success(mocker, client, request_factory):
    """Test that a POST request with valid book data creates a new book and returns 201 status code"""
    url = reverse('add-book')
    # create a new category
    view = AddBookAPIView.as_view()
    category = Category.objects.create(name='Test Category')
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'publisher': 'Abi Press',
        'category': category.id,
    }
    mocker.patch("api.views.publish_save_book_event", return_value=None)
    request = request_factory.post(url, data, format='json')
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert "Book added successfully" in response.data.get("message")
    


def test_with_bad_data(mocker, request_factory, bad_data):  
    """Test with bad data should return 400 status code
    """
    url = reverse('add-book')
    view = AddBookAPIView.as_view()
    
    mocker.patch("api.views.publish_save_book_event", return_value=None)
    request = request_factory.post(url, bad_data, format='json')
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_add_book_with_nonexistent_category_id(mocker, client, request_factory):
    """Test that a POST request with non-existent category ID returns 400 status code"""
    url = reverse('add-book')
    view = AddBookAPIView.as_view()
    category = Category.objects.create(name='Test Category')
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'publisher': 'Abi Press',
        'category': 2,
    }
    mocker.patch("api.views.publish_save_book_event", return_value=None)
    request = request_factory.post(url, data, format='json')
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.django_db
def test_add_book_with_internal_server_error(mocker, client, request_factory):
    """Test that a POST request with non-existent category ID returns 400 status code"""
    url = reverse('add-book')
    view = AddBookAPIView.as_view()
    category = Category.objects.create(name='Test Category')
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'publisher': 'Abi Press',
        'category': category.id,
    }
    mocker.patch("api.views.publish_save_book_event", return_value=None)
    mocker.patch("api.views.AddBookAPIView.serializer_class.save", side_effect=Exception("Test Exception"))
    request = request_factory.post(url, data, format='json')
    response = view(request)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Something went wrong" in response.data.get("message")
  
@pytest.mark.django_db
def test_get_books_not_available_returns_correct_status_code(mocker, client, request_factory):
    url = reverse('books-unavailable')
    view = BookNotAvailableListAPIView.as_view()
    
    category = Category.objects.create(name='Test Category')
    # create some books
    Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    Book.objects.create(title='Book 2', author="Test Author", available=False, publisher="Press Ltd", category=category)
    Book.objects.create(title='Book 3', author="Test Author", publisher="Press Ltd", category=category)
    
    request = request_factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert "List of books not available" == response.data.get("message")
    assert "success" == response.data.get("status")
    assert 2 == len(response.data.get("data"))
    assert response.data.get("data")[0]["title"] == "Book 1"
    assert response.data.get("data")[1]["title"] == "Book 2"
    
  
@pytest.mark.django_db
def test_get_books_not_available_returns_empty_list(mocker, client, request_factory):
    url = reverse("books-unavailable")
    view = BookNotAvailableListAPIView.as_view()
    
    request = request_factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert "List of books not available" == response.data.get("message")
    assert "success" == response.data.get("status")
    assert 0 == len(response.data.get("data"))
    
@pytest.mark.django_db
def test_get_users_and_their_borrowed_books_with_no_users(client, request_factory):
    url = reverse('users')
    view = ListUsersAPIView.as_view()
    
    request = request_factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert "List of users and their borrowed books" == response.data.get("message")
    assert "success" == response.data.get("status")
    assert 0 == len(response.data.get("data"))


@pytest.mark.django_db
def test_get_users_and_their_borrowed_books_with_users_having_no_borrowed_books(client, request_factory):
    url = reverse('users')
    view = ListUsersAPIView.as_view()
    
    # create users
    user1 = User.objects.create(email='user1@gmail.com', first_name="Test user 1", last_name="Test 1", password="password")
    user2 = User.objects.create(email='user2@gmail.com', first_name="Test user 2", last_name="Test 2", password="password")
    
    request = request_factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert "List of users and their borrowed books" == response.data.get("message")
    assert "success" == response.data.get("status")
    assert 2 == len(response.data.get("data"))
    assert response.data.get("data")[0]["email"] == "user1@gmail.com"
    assert response.data.get("data")[1]["email"] == "user2@gmail.com"
    assert 0 == len(response.data.get("data")[0]["borrowed_books"])
    assert 0 == len(response.data.get("data")[1]["borrowed_books"])
    
@pytest.mark.django_db
def test_get_users_and_their_borrowed_books_with_multiple_books(client, request_factory):
    url = reverse('users')
    view = ListUsersAPIView.as_view()
    return_date = date.today() + timedelta(days=3)
    
    # create users and borrowed books
    user1 = User.objects.create(email='user1@gmail.com', first_name="Test user 1", last_name="Test 1", password="password")
    user2 = User.objects.create(email='user2@gmail.com', first_name="Test user 2", last_name="Test 2", password="password")
    category = Category.objects.create(name='Test Category')
    book1 = Book.objects.create(title='Book 1', author='Test Author', publisher='Press Ltd', category=category)
    book2 = Book.objects.create(title='Book 2', author='Test Author', publisher='Press Ltd', category=category)
    book3 = Book.objects.create(title='Book 3', author='Test Author', publisher='Press Ltd', category=category)
    BorrowedBookLog.objects.create(borrower=user1, book=book1, return_date=return_date)
    BorrowedBookLog.objects.create(borrower=user1, book=book2, return_date=return_date)
    BorrowedBookLog.objects.create(borrower=user2, book=book3, return_date=return_date)
    
    request = request_factory.get(url)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert "List of users and their borrowed books" == response.data.get("message")
    assert "success" == response.data.get("status")
    assert 2 == len(response.data.get("data"))
    assert response.data.get("data")[0]["full_name"] == "Test user 1 Test 1"
    assert 2 == len(response.data.get("data")[0]["borrowed_books"])
    assert response.data.get("data")[0]["borrowed_books"][0]["book_title"] == "Book 1"
    assert response.data.get("data")[0]["borrowed_books"][1]["book_title"] == "Book 2"
    assert response.data.get("data")[1]["email"] == "user2@gmail.com"
    assert 1 == len(response.data.get("data")[1]["borrowed_books"])
    assert response.data.get("data")[1]["borrowed_books"][0]["book_title"] == "Book 3"
    
@pytest.mark.django_db
def test_delete_book_not_existing(mocker, client, request_factory):
    url = reverse('delete-book', kwargs={'id': 1})
    view = DeleteBookAPIView.as_view()

    mocker.patch("api.views.publish_delete_event", return_value=None)
    request = request_factory.delete(url)
    response = view(request, id=1)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Book matching query does not exist." in response.data.get("message")
    
@pytest.mark.django_db
def test_delete_book_success(mocker, client, request_factory):
    """ Delete a book
    """
    # create the book object
    category = Category.objects.create(name='Test Category')
    book1 = Book.objects.create(title='Book 1', author='Test Author', publisher='Press Ltd', category=category)
    url = reverse('delete-book', kwargs={'id': book1.id})
    view = DeleteBookAPIView.as_view()
    mocker.patch("api.views.publish_delete_event", return_value=None)
    request = request_factory.delete(url)
    response = view(request, id=1)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "Book deleted successfully" in response.data.get("message")
    assert "success" == response.data.get("status")