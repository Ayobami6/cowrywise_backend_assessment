from django.urls import path
from .views import AddBookAPIView, BookNotAvailableListAPIView, ListUsersAPIView, DeleteBookAPIView

urlpatterns = [
    path("books", AddBookAPIView.as_view(), name="add-book"),
    path("books/unavailable", BookNotAvailableListAPIView.as_view(), name="books-unavailable"),
    path("users", ListUsersAPIView.as_view(), name="users"),
    path("books/<int:id>", DeleteBookAPIView.as_view(), name="delete-book"),
]
