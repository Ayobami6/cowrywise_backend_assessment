import redis
import threading
import time

r = redis.Redis(host="redis_service", port=6379)

print("After redis connection")


def listen_save_user_event():
    
    pubsub = r.pubsub()
    pubsub.subscribe('save-user')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            user_data = message['data'].decode('utf-8')
            save_user_to_database(user_data)
            
def save_user_to_database(user_data):
    print(f"Saved user data: {user_data}")


def start_listening():
    print("Waiting for messages from publishers.... press Ctrl+C to cancel")
    listen_save_user_event()
    
