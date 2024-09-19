from django.shortcuts import render
from sparky_utils.response import service_response
from rest_framework.views import APIView
import json
# from .producer import publish
from .publisher import publish_save_user_event


# Create your views here.


class RootPage(APIView):
    
    def get(self, request, format=None):
        publish_save_user_event(json.dumps({"email": "ayobamidele02+2@gmail.com", "first_name": "Ayobami", "last_name": "Alaran", "password":"password"}))
        return service_response(
            status="success", message="Great, Welcome all good!", status_code=200
        )
