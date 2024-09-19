import redis
import threading
import time
import json
from django.contrib.auth import get_user_model
from typing import Any
from .models import Book, BorrowedBookLog


User = get_user_model()

r = redis.Redis(host="redis_service", port=6379)

print("After redis connection")


def listen_to_event():
    
    pubsub = r.pubsub()
    pubsub.subscribe('save-user', 'log-borrow-book')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            if message["channel"] == b'save-user':
                save_user_to_database(data)
            elif message["channel"] == b'log-borrow-book':
                log_borrowed_book(data)
            
def save_user_to_database(user_data):
    data = json.loads(user_data)
    user = User.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
    user.save()
    print(f"Saved user data!!: {user}")


def log_borrowed_book(event_data: Any):
    data = json.loads(event_data)
    book = Book.objects.get(id=int(data['book']))
    borrower = User.objects.get(id=int(data['borrower']))
    BorrowedBookLog.objects.create(book=book, borrower=borrower, borrow_date=data['borrow_date'], return_date=data['return_date'])
    print(f"Logged borrowed book: {book} for user: {borrower}")
    

def start_listening():
    print("Waiting for messages from publishers.... press Ctrl+C to cancel")
    listen_to_event()
    
