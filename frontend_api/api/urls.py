from django.urls import path
from .views import EnrollUserAPIView

urlpatterns = [
    path("users/enroll", EnrollUserAPIView.as_view(), name="enroll-user"),
]
