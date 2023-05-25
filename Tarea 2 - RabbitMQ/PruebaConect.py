import pika

credentials = pika.PlainCredentials('user', 'password')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

try:
    connection = pika.BlockingConnection(parameters)
    print("Connected to RabbitMQ")
    connection.close()
except pika.exceptions.AMQPConnectionError:
    print("Failed to connect to RabbitMQ")
