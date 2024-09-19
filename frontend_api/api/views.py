from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from .serializers import BookSerializer, CreateUserSerializer
from utils.advice import exception_advice
import json
from .publisher import publish_save_user_event, publish_log_borrow_book
from rest_framework import viewsets
from .models import Book, User, BorrowedBookLog
from django.db.models import Q
from datetime import timedelta, datetime, date
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
            data = serializer.data
            data.pop("password")
            return service_response(
                status="success",
                message="User enrolled successfully!",
                data=data,
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
        book = Book.objects.get(id=kwargs.get('pk'))
        serializer = self.serializer_class(book)
        return service_response(status="success", message="Book Fetched Successfully", data=serializer.data, status_code=200)


class BorrowBookAPIView(APIView):
    """User Books Borrowing Api handler
    """
    
    @exception_advice
    def post(self, request, *args, **kwargs):
        """Post handler to handle book borrowing requests
        """
        # get book id
        book_id = kwargs.get('id')
        # get user id
        user_id = request.data.get('user_id')
        duration = request.data.get('duration')
        # check if book exists
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return service_response(status="error", message="Book not found", status_code=404)
        
        # check if user exists
        user = User.objects.filter(id=user_id).first()
        if not user:
            return service_response(status="error", message="You are not enrolled to the library", status_code=404)
        
        # check if user has borrowed the book
        if not book.available:
            return service_response(status="error", message="User has already borrowed this book", status_code=409)
        
        # borrow the book
        now = date.today()
        return_date = now + timedelta(days=int(duration))
        book.available = False
        book.available_date = return_date
        book.save()
        # create log
        log_data = {
            "book": book,
            "borrower": user,
            "borrow_date": now,
            "return_date": return_date,
        }
        BorrowedBookLog.objects.create(**log_data)
        event_data = {
            "book": book.id,
            "borrower": user.id,
            "borrow_date": str(now),
            "return_date": str(return_date),
            
        }
        # publish log_data
        publish_log_borrow_book(json.dumps(event_data))
        return service_response(status="success", message="Book borrowed successfully", data=book.id, status_code=200)