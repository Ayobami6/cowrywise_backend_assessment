from config import channel

channel.queue_declare(queue="add-book")


def callback(ch, method, properties, body):
    print("Messaged received")
    print(body)
    

channel.basic_consume(queue="add-book", on_message_callback=callback, auto_ack=True)

print("Waiting for messages from producer.... press Ctrl + C to cancel")

channel.start_consuming()

channel.close()

