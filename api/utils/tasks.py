import pika

def send_message_to_rabbitmq(queue_name, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', 
            port = 5672
            )
        )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='', 
        routing_key=queue_name, 
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()