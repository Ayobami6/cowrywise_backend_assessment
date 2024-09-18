import pika

params = pika.URLParameters("amqp://guest:guest@rabbitmq:5672/")

connection = pika.BlockingConnection(params)

channel = connection.channel()

print("Waiting for connection!!!!")

