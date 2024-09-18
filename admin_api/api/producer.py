from config import channel


def publish():
    channel.basic_publish(exchange="", routing_key="save-user", body="Save User")