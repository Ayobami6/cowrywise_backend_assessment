from django.urls import path
from .views import AddBookAPIView

urlpatterns = [
    path("books", AddBookAPIView.as_view(), name="add-book"),
]
