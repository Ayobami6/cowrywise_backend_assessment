from django.test import TestCase
import pytest
from rest_framework.test import APIRequestFactory, APIClient
from django.urls import reverse
from .models import Book, Category, User, BorrowedBookLog
from .views import BorrowBookAPIView, EnrollUserAPIView
from rest_framework.response import Response
from sparky_utils.response import service_response
from datetime import date, timedelta
# Create your tests here.


@pytest.fixture
def request_factory():
    return APIRequestFactory()
    

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user_payload():
    return {
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'first_name': 'test',
        'last_name': 'user'
    }
    
@pytest.fixture
def invalid_payload():
    return {
        'password': '',
        'first_name': '',
        'last_name': ''
    }
    
@pytest.fixture
def mock_books():
    return [
        {
            "id": 1,
            "title": "Rumple",
            "author": "Ayo",
            "publisher": "Print Press",
            "available": True,
            "available_date": None,
            "category": 1
        },
        {
            "id": 2,
            "title": "Rumplesti",
            "author": "Ayo",
            "publisher": "Print Press",
            "available": True,
            "available_date": None,
            "category": 1
        }
    ]


@pytest.mark.django_db
def test_enroll_user_success(mocker, create_user_payload, request_factory):
    """Test user enrollment success to the library
    """
    # Mock user creation
    mocker.patch('api.views.publish_save_user_event', return_value=None)
    url = reverse("enroll-user")
    view = EnrollUserAPIView.as_view()
    request = request_factory.post(url, create_user_payload)
    response = view(request)
    assert response.status_code == 201
    assert response.data.get("status") == "success"
    

@pytest.mark.django_db
def test_unique_email(mocker, request_factory, create_user_payload):
    """Test user enrollment fails due to unique email
    """
    # Mock user creation
    mocker.patch('api.views.publish_save_user_event', return_value=None)
    url = reverse("enroll-user")
    view = EnrollUserAPIView.as_view()
    request1 = request_factory.post(url, create_user_payload)
    request2 = request_factory.post(url, create_user_payload)
    view(request1)
    response = view(request2)
    assert response.status_code == 409
    assert response.data.get("status") == "error"
    assert response.data.get("message") == "Email already exists"
    

@pytest.mark.django_db
def test_invalid_payload(mocker, request_factory, invalid_payload):
    """Test user enrollment fails due to invalid payload
    """
    # Mock user creation
    mocker.patch('api.views.publish_save_user_event', return_value=None)
    url = reverse("enroll-user")
    view = EnrollUserAPIView.as_view()
    request = request_factory.post(url, invalid_payload)
    response = view(request)
    assert response.status_code == 400
    assert response.data.get("status") == "error"
    assert isinstance(response.data.get("message"), dict)

@pytest.mark.django_db
def test_book_list_with_nonexistent_publisher(mocker, client, mock_books):
    """Test book list with non-existent publisher
    """
    # Mock service response
    # mocker.patch('api.views.service_response', return_value=Response(status=200, data=mock_books))
    response = client.get('/api/v1/books?publisher=NonExistentPublisher')
    
    # Assert the response status code and data
    assert response.status_code == 200
    assert response.data.get('status') == 'success'
    assert response.data.get('message') == 'Book Fetched Successfully'
    assert len(response.data.get('data')) == 0
    
@pytest.mark.django_db
def test_book_list_with_valid_publisher(mocker, client, mock_books):
    """Test book list with valid publisher
    """
    # Mock service response
    # mocker.patch('api.views.service_response', return_value=Response(status=200, data=mock_books))
    category = Category.objects.create(name='Test Category')
    # create some books
    Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    Book.objects.create(title='Book 2', author="Test Author", available=False, publisher="Print Press", category=category)
    response = client.get('/api/v1/books?publisher=Print Press')
    
    # Assert the response status code and data
    assert response.status_code == 200
    assert response.data.get('status') == 'success'
    assert response.data.get('message') == 'Book Fetched Successfully'
    assert len(response.data.get('data')) == 1
    
    
@pytest.mark.django_db
def test_book_list_with_valid_category(mocker, client, mock_books):
    """Test book list with valid category
    """
    # mocker.patch('api.views.service_response', return_value=Response(status=200, data=mock_books))
    category = Category.objects.create(name='Test Category')
    # create some books
    Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    Book.objects.create(title='Book 2', author="Test Author", available=False, publisher="Print Press", category=category)
    response = client.get(f'/api/v1/books?category={category.pk}')
    
    # Assert the response status code and data
    assert response.status_code == 200
    assert response.data.get('status') == 'success'
    assert response.data.get('message') == 'Book Fetched Successfully'
    assert len(response.data.get("data")) == 2
    

@pytest.mark.django_db
def test_list_all_available_books(mocker, client, request_factory):
    """List all available books
    """
    response = client.get(f'/api/v1/books')
    
    # Assert the response status code and data
    assert response.status_code == 200
    assert response.data.get('status') == 'success'
    assert response.data.get('message') == 'Book Fetched Successfully'
    assert len(response.data.get("data")) == 0
    
    
@pytest.mark.django_db
def test_handle_internal_server_gracefully(mocker, client):
    """Test internal server exception handle
    """
    mocker.patch("api.views.Book.objects.all", side_effect=Exception("Test Exception"))
    response = client.get(f'/api/v1/books')
    assert response.status_code == 500
    assert response.data.get('status') == 'error'
    assert response.data.get('message') == 'Something went wrong'


@pytest.mark.django_db
def test_book_retrieve_notfound(mocker, client, request_factory):
    response = client.get(f'/api/v1/books/1')
    assert response.status_code == 404
    assert response.data.get('status') == 'error'


@pytest.mark.django_db
def test_book_retrieve_success(mocker, client, request_factory):
    category = Category.objects.create(name='Test Category')
    # create some books
    Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    response = client.get(f'/api/v1/books/{category.id}')
    assert response.status_code == 200
    assert response.data.get('status') == 'success'

@pytest.mark.django_db
def test_borrow_book_nonexistent_book(mocker, client, request_factory):
    """Test book borrowing with non-existent book id
    """
    mocker.patch('api.views.publish_log_borrow_book', return_value=None)
    
    # Create a user
    user = User.objects.create(email='testuser@example.com', password='testpassword123', first_name='test', last_name='user')
    
    # Send a POST request to borrow a non-existent book
    url = reverse("borrow", kwargs={'id': 1})
    data = {"user_id": user.id, "duration": 7}
    response = client.post(url, data)
    
    # Assert the response status code and data
    assert response.status_code == 404
    assert response.data.get("status") == "error"
    assert response.data.get("message") == "Book not found"
    

@pytest.mark.django_db
def test_borrow_user_not_exist(mocker, request_factory, client):
    """Test book borrowing with non-existent user id
    """
    mocker.patch('api.views.publish_log_borrow_book', return_value=None)
    
    category = Category.objects.create(name='Test Category')
    # create some books
    book = Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    
    # Send a POST request to borrow a book
    url = reverse("borrow", kwargs={'id': book.id})
    data = {"user_id": 1, "duration": 7}
    response = client.post(url, data)
    
    # Assert the response status code and data
    assert response.status_code == 404
    assert response.data.get("status") == "error"
    assert response.data.get("message") == "You are not enrolled to the library"
    
    

@pytest.mark.django_db
def test_borrow_book_borrow_success(mocker, request_factory, client):
    """Test book borrowing with an already borrowed book
    """
    mocker.patch('api.views.publish_log_borrow_book', return_value=None)
    
    category = Category.objects.create(name='Test Category')
    # create some books
    book = Book.objects.create(title='Book 1', author="Test Author", available=True, publisher="Press Ltd", category=category)
    
    # Create a user and borrow the book
    user = User.objects.create(email='testuser@example.com', password='testpassword123', first_name='test', last_name='user')
    
    # Send a POST request to borrow the book again
    url = f"/api/v1/books/borrow/{book.id}"
    data = {"user_id": user.id, "duration": 7}
    response = client.post(url, data)
    borrowed_book = BorrowedBookLog.objects.get(book=book)
    return_date = date.today() + timedelta(days=7)
    assert response.status_code == 200
    assert response.data.get("status") == "success"
    assert borrowed_book.borrow_date == date.today()
    assert borrowed_book.return_date == return_date
    

@pytest.mark.django_db
def test_book_unavailable(mocker, client):
    """Test book availability
    """
    category = Category.objects.create(name='Test Category')
    # create some books
    book = Book.objects.create(title='Book 1', author="Test Author", available=False, publisher="Press Ltd", category=category)
    
    # Create a user and borrow the book
    user = User.objects.create(email='testuser@example.com', password='testpassword123', first_name='test', last_name='user')
    url = reverse("borrow", kwargs={'id': book.id})
    data = {"user_id": user.id, "duration": 7}
    response = client.post(url, data)
    
    # Assert the response status code and data
    assert response.status_code == 409
    assert response.data.get("status") == "error"
    assert response.data.get("message") == "User has already borrowed this book"
    
