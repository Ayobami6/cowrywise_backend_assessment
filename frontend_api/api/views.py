from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from .serializers import BookSerializer, CreateUserSerializer
from utils.advice import exception_advice
import json
from .publisher import publish_save_user_event
from rest_framework import viewsets
from .models import Book
from django.db.models import Q
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
            serializer.save()
            # publish the serializer.data
            publish_save_user_event(json.dumps(serializer.data))
            return service_response(
                status="success",
                message="User enrolled successfully!",
                status_code=201,
            )   
        return service_response(status="error", message=serializer.errors, status_code=400)
    

class BookAPIViewSet(viewsets.ModelViewSet):
    queryset =  Book.objects.all()
    serializer_class = BookSerializer
    
    @exception_advice
    def list(self, request, *args, **kwargs):
        # get all books
        books = Book.objects.all()
        # add all filter query
        publisher = request.query_params.get('publisher')
        category = request.query_params.get('category')
        if publisher:
            books = books.filter(Q(publisher__icontains=publisher))
        if category:
            books = books.filter(category=int(category))
        
        serializer = self.serializer_class(books, many=True)
        return service_response(status="success", message="Book Fetched Successfully", data=serializer.data, status_code=200)
    
    
    @exception_advice
    def retrieve(self, request, *args, **kwargs):
        # id = kwargs.get('id')
        book = Book.objects.get(id=kwargs.get('id'))
        serializer = self.serializer_class(book)
        return service_response(status="success", message="Book Fetched Successfully", data=serializer.data, status_code=200)
        