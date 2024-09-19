from django.urls import path, include
from .views import EnrollUserAPIView, BookAPIViewSet, BorrowBookAPIView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)

router.register("books", BookAPIViewSet, basename="books")

urlpatterns = [
    path("users/enroll", EnrollUserAPIView.as_view(), name="enroll-user"),
    path("books/borrow/<int:id>", BorrowBookAPIView.as_view(), name="borrow"),
    path("", include(router.urls)),
]
