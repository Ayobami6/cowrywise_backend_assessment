import pika

connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq:5672/"))

channel = connection.channel()


def publish():
    channel.basic_publish(exchange="", routing_key="add-book", body="Add a new book, comprehende?")

