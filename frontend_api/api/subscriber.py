import redis
import threading
import time
import json
from django.contrib.auth import get_user_model
from .models import Book, Category

User = get_user_model()

r = redis.Redis(host="redis_service", port=6379)

print("After redis connection")

# listen to add book to db
def listen_add_book_event():
    pubsub = r.pubsub()
    pubsub.subscribe('add-book', 'delete-book')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            book_data = message['data'].decode('utf-8')
            if message["channel"] == b'add-book':
                save_book_to_database(book_data)
            elif message["channel"] == b'delete-book':
                delete_book_from_database(book_data)
            
def save_book_to_database(book_data):
    data = json.loads(book_data)
    category = Category.objects.get(id=int(data['category']))
    book = Book.objects.create(title=data['title'], author=data['author'], category=category, publisher=data['publisher'])
    print(f"Saved book data!!: {book}")
    
    
def delete_book_from_database(book_data):
    data = json.loads(book_data)
    book = Book.objects.get(id=int(data['id']))
    book.delete()
    print(f"Deleted book data!!: {book}")

def start_listening():
    print("Waiting for messages from publishers.... press Ctrl+C to cancel")
    listen_add_book_event()
