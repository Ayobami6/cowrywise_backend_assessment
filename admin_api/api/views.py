from django.shortcuts import render
from sparky_utils.response import service_response
from rest_framework.views import APIView
import json
# from .producer import publish
from .publisher import publish_save_book_event, publish_delete_event
from utils.advice import exception_advice
from .serializers import AddBookSerializer, GetBookSerializer, GetUserSerializer
from .models import Book, User

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
        

class ListUsersAPIView(APIView):
    """List user and their borrowed books
    """
    
    @exception_advice
    def get(self, request, *args, **kwargs):
        """Get handler to list users and their borrowed books
        """
        # get users and their borrowed books
        users = User.objects.all()
        serializer = GetUserSerializer(users, many=True)
        return service_response(
            status="success", message="List of users and their borrowed books", data=serializer.data, status_code=200
        )
             

#TODO: delete a book and persist in the frontend service Db
class DeleteBookAPIView(APIView):
    """Delete a book
    """
    
    @exception_advice
    def delete(self, request, *args, **kwargs):
        """Delete handler to delete a book
        """
        book_id = kwargs.get('id')
        book = Book.objects.get(id=book_id)
        book.delete()
        # publish delete book event
        event_data = {
            "id": book_id
        }
        publish_delete_event(json.dumps(event_data))
        return service_response(
            status="success", message="Book deleted successfully", status_code=204
        )
