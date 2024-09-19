from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from .serializers import CreateUserSerializer
from utils.exceptions import exception_advice
import json
from .publisher import publish_save_user_event
# Create your views here.


class RootPage(APIView):
    def get(self, request):
        return service_response(
            status="success",
            message="Welcome to the Cowrywise Client API!",
            status_code=200,
        )
        


class EnrollUserAPIView(APIView):
    """Enrolls a user to the library
    """    
    serializer_class = CreateUserSerializer
    
    @exception_advice
    def post(self, request, *args, **kwargs):
        """Enroll a user post handler
        """
        serializer: CreateUserSerializer = self.serializer_class(data=request.data)   
        if serializer.is_valid():
            saved_user = serializer.save()
            # publish the serializer.data
            publish_save_user_event(json.dumps(saved_user))
            return service_response(
                status="success",
                message="User enrolled successfully!",
                status_code=201,
            )   
        return service_response(status="error", message=serializer.errors, status_code=400)