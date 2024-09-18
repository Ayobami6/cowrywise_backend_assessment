import pika

connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq:5672/"))
channel = connection.channel()

channel.queue_declare(queue='save-user')


def publish():
    channel.basic_publish(exchange="", routing_key="save-user", body="Save User")
    print(" [x] Sent 'Hello World!'")
    connection.close()
