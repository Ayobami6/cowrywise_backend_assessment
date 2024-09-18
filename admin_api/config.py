import pika

params = pika.URLParameters("amqps://guest:guest@rabbitmq_service:5672/")

connection = pika.BlockingConnection(params)

channel = connection.channel()


