from django.urls import path, include
from .views import EnrollUserAPIView, BookAPIViewSet
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)

router.register("books", BookAPIViewSet, basename="books")

urlpatterns = [
    path("users/enroll", EnrollUserAPIView.as_view(), name="enroll-user"),
    path("", include(router.urls)),
]
