from django.shortcuts import render
from sparky_utils.response import service_response
from rest_framework.views import APIView
import json
# from .producer import publish
from .publisher import publish_save_book_event
from utils.advice import exception_advice
from .serializers import AddBookSerializer, GetBookSerializer
from .models import Book

# Create your views here.


class RootPage(APIView):
    
    def get(self, request, format=None):
        return service_response(
            status="success", message="Great, Welcome all good!", status_code=200
        )

class AddBookAPIView(APIView):
    """Add a new book to the catalogue
    """
    serializer_class = AddBookSerializer
    
    @exception_advice
    def post(self, request, *args, **kwargs):
        """Post handler to add a new book to the catalogue
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # publish()
            publish_save_book_event(json.dumps(serializer.data))
            return service_response(
                status="success", message="Book added successfully", data=serializer.data, status_code=201
            )
        return service_response(status="success", message=serializer.errors, status_code=400)


class BookNotAvailableListAPIView(APIView):
    """List all books not available
    """
    serializer_class = GetBookSerializer
    @exception_advice
    def get(self, request, *args, **kwargs):
        """Get handler to list all books not available
        """
        # filter books not available
        books_not_available = Book.objects.filter(available=False)
        serializer = self.serializer_class(books_not_available, many=True)
        return service_response(
            status="success", message="List of books not available", data=serializer.data, status_code=200
        )
        
