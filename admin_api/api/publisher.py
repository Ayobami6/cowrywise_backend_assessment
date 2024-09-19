import redis
from typing import Any

r = redis.Redis(host="redis_service", port=6379)

def publish_save_user_event(event_data: Any) -> None:
    r.publish("add-book", event_data)
