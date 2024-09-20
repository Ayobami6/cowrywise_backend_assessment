from django.test import TestCase
import pytest
from rest_framework.test import APIRequestFactory, APIClient
from django.urls import reverse
from .views import EnrollUserAPIView
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

