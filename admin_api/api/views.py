from django.shortcuts import render
from sparky_utils.response import service_response
from rest_framework.views import APIView
from .producer import publish


# Create your views here.


class RootPage(APIView):
    
    def get(self, request, format=None):
        publish()
        return service_response(
            status="success", message="Great, Welcome all good!", status_code=200
        )
