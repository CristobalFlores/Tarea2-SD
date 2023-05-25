import pika
import json
import os
import time
from threading import Thread
import argparse
import matplotlib.pyplot as plt
from threading import Timer

# Variable global para almacenar los datos de rendimiento
latencies = []

class Consumer(Thread):
    def __init__(self, consumer_id, category, location, rabbitmq_host, rabbitmq_user, rabbitmq_pass):
        Thread.__init__(self)
        self.consumer_id = consumer_id
        self.category = category
        self.location = location
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass

    def run(self):
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
        parameters = pika.ConnectionParameters(self.rabbitmq_host, 5672, '/', credentials)

        try:
            connection = pika.BlockingConnection(parameters)
            print(f"Consumer {self.consumer_id}: Conectado a RabbitMQ")
            channel = connection.channel()
            channel.exchange_declare(exchange='topics', exchange_type='topic')

            result = channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue

            binding_key = f"device.{self.category}.{self.location}"
            channel.queue_bind(exchange='topics', queue=queue_name, routing_key=binding_key)

            def callback(ch, method, properties, body):
                message = json.loads(body)
                print(f"Consumer {self.consumer_id} recibe: {message} desde el routing_key {method.routing_key}")

                send_time = message['timestamp']  # Timestamp de envío del mensaje
                receive_time = time.time()  # Timestamp de recepción del mensaje
                latency = receive_time - send_time  # Cálculo de latencia
                latencies.append(latency)
                print(f"Consumer {self.consumer_id} - Latencia: {latency} segundos")

            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=True
            )

            print(f"Consumer {self.consumer_id} esperando mensajes en {binding_key} cola...")
            channel.start_consuming()

            connection.close()
        except pika.exceptions.AMQPConnectionError:
            print(f"Consumer {self.consumer_id}: Fallo de conexión a RabbitMQ")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Consumir mensajes de RabbitMQ.')
parser.add_argument('--num_consumers', type=int, default=1, help='Numero de consumers por categoria y ubicacion')
args = parser.parse_args()

rabbitmq_host = "localhost"
rabbitmq_user = "user"
rabbitmq_pass = "password"
categories = ["Category1", "Category2", "Category3", "Category4", "Category5"]
locations = ["Location1", "Location2", "Location3"]

consumer_id = 0
num_consumers = args.num_consumers
consumers_per_category = num_consumers // len(categories)
consumers_per_location = num_consumers // len(locations)

for category in categories:
    for _ in range(consumers_per_category):
        Consumer(consumer_id, category, "*", rabbitmq_host, rabbitmq_user, rabbitmq_pass).start()
        consumer_id += 1

for location in locations:
    for _ in range(consumers_per_location):
        Consumer(consumer_id, "*", location, rabbitmq_host, rabbitmq_user, rabbitmq_pass).start()
        consumer_id += 1

# Función para el trazado de datos
def plot_data():
    plt.figure(figsize=(10, 6))
    plt.plot(latencies)
    plt.xlabel('Mensaje')
    plt.ylabel('Latencia (segundos)')
    plt.title('Latencia de mensajes - Consumidor')

    plt.tight_layout()
    plt.show()

    # Re-programar la función para que se ejecute después de otro intervalo
    timer = Timer(60.0, plot_data)  # 60.0 segundos
    timer.start()

# Iniciar el temporizador por primera vez
timer = Timer(60.0, plot_data)  # 60.0 segundos
timer.start()


##################################################################
## Esto es de prueba cuando se levata el Contenedor del Consumidor
##################################################################

rabbitmq_host = os.getenv("RABBITMQ_HOST")  # Modificar esto
rabbitmq_user = os.getenv("RABBITMQ_USER")  # Modificar esto
rabbitmq_pass = os.getenv("RABBITMQ_PASS")  # Modificar esto