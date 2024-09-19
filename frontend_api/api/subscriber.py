import redis
import threading
import time
import json
from django.contrib.auth import get_user_model

User = get_user_model()

r = redis.Redis(host="redis_service", port=6379)

print("After redis connection")

# listen to add book to db
def listen_add_book_event():
    pubsub = r.pubsub()
    pubsub.subscribe('add-book')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            book_data = message['data'].decode('utf-8')
            save_book_to_database(book_data)
            
def save_book_to_database(book_data):
    data = json.loads(book_data)
    print(f"Saved book data!!: {data}")

def start_listening():
    print("Waiting for messages from publishers.... press Ctrl+C to cancel")
    listen_add_book_event()
