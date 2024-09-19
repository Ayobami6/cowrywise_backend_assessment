import redis
from typing import Any

r = redis.Redis(host="redis_service", port=6379)

def publish_save_user_event(event_data: Any) -> None:
    r.publish("save-user", event_data)


def publish_log_borrow_book(log_data: Any) -> None:
    r.publish("log-borrow-book", log_data)
    
