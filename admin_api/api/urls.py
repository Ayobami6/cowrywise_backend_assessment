from django.urls import path
from .views import AddBookAPIView, BookNotAvailableListAPIView

urlpatterns = [
    path("books", AddBookAPIView.as_view(), name="add-book"),
    path("books/unavailable", BookNotAvailableListAPIView.as_view(), name="books-unavailable"),
]
