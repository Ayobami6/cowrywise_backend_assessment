import redis
import threading
import time
import json
from django.contrib.auth import get_user_model

User = get_user_model()

r = redis.Redis(host="redis_service", port=6379)

print("After redis connection")

# listen to add book to db
def listen_save_user_event():
    pubsub = r.pubsub()
    pubsub.subscribe('add-book')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            user_data = message['data'].decode('utf-8')
            save_user_to_database(user_data)
            
def save_user_to_database(user_data):
    data = json.loads(user_data)
    user = User.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
    print(f"Saved user data!!: {user}")

def start_listening():
    print("Waiting for messages from publishers.... press Ctrl+C to cancel")
    listen_save_user_event()
