import pika

params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest'),
    ssl_options=None
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


print("Channel Created!")