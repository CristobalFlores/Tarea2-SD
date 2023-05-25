import pika
import json
import time
import os
from threading import Thread
from random import randint, choice
from string import ascii_letters
import argparse
import matplotlib.pyplot as plt
from threading import Timer

# Variables globales para almacenar los datos de rendimiento
latencies = []
message_rates = []

class Device(Thread):
    def __init__(self, device_id, category, location, delta_time, rabbitmq_host, rabbitmq_user, rabbitmq_pass):
        Thread.__init__(self)
        self.device_id = device_id
        self.category = category
        self.location = location
        self.delta_time = delta_time
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass

    def run(self):
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
        parameters = pika.ConnectionParameters(self.rabbitmq_host, 5672, '/', credentials)

        try:
            connection = pika.BlockingConnection(parameters)
            print(f"Dispositivo {self.device_id}: Conectado a RabbitMQ")
            channel = connection.channel()
            channel.exchange_declare(exchange='topics', exchange_type='topic')

            message_count = 0  # Contador de mensajes enviados
            start_time = time.time()  # Tiempo de inicio

            while True:
                time.sleep(self.delta_time)
                send_time = time.time()  # Timestamp de envío del mensaje

                message = {
                    'timestamp': send_time,
                    'value': {
                        'data': ''.join(choice(ascii_letters) for i in range(randint(10, 50)))
                    }
                }

                routing_key = f"device.{self.category}.{self.location}"
                channel.basic_publish(
                    exchange='topics',
                    routing_key=routing_key,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(content_type='application/json')
                )
                print(f"Dispositivo {self.device_id} envia: {message} con routing key {routing_key}")

                latency = time.time() - send_time  # Cálculo de latencia
                latencies.append(latency)
                print(f"Dispositivo {self.device_id} - Tiempo de latencia: {latency} segundos")

                message_count += 1  # Incremento del contador de mensajes enviados
                end_time = time.time()  # Tiempo de finalización
                elapsed_time = end_time - start_time  # Tiempo transcurrido
                message_rate = message_count / elapsed_time  # Tasa de mensajes por segundo
                message_rates.append(message_rate)
                print(f"Dispositivo {self.device_id} - Tasa de mensajes: {message_rate} mensajes/segundo")

            connection.close()
        except pika.exceptions.AMQPConnectionError:
            print(f"Dispositivo {self.device_id}: Fallo con la conexión a RabbitMQ")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Produce messages for RabbitMQ.')
parser.add_argument('--num_dispo', type=int, default=10, help='Numero de dispositivos a simular')
parser.add_argument('--delta_time', type=int, default=5, help='Intervalo entre mensajes en segundos')
args = parser.parse_args()

rabbitmq_host = "localhost"
rabbitmq_user = "user"
rabbitmq_pass = "password"
categories = ["Category1", "Category2", "Category3", "Category4", "Category5"]
locations = ["Location1", "Location2", "Location3"]

for i in range(args.num_dispo):  # Simulate num_devices devices
    Device(i, choice(categories), choice(locations), args.delta_time, rabbitmq_host, rabbitmq_user, rabbitmq_pass).start()

# Función para el trazado de datos
def plot_data():
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(latencies)
    plt.xlabel('Mensaje')
    plt.ylabel('Latencia (segundos)')
    plt.title('Latencia de mensajes - Productor')

    plt.subplot(2, 1, 2)
    plt.plot(message_rates)
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Tasa de mensajes (mensajes/segundo)')
    plt.title('Tasa de mensajes - Productor')

    plt.tight_layout()
    plt.show()

    # Re-programar la función para que se ejecute después de otro intervalo
    timer = Timer(60.0, plot_data)  # 60.0 segundos
    timer.start()

# Iniciar el temporizador por primera vez
timer = Timer(60.0, plot_data)  # 60.0 segundos
timer.start()

##################################################################
## Esto es de prueba cuando se levata el Contenedor del Productor
##################################################################
rabbitmq_host = os.getenv("RABBITMQ_HOST")  # Modificar esto
rabbitmq_user = os.getenv("RABBITMQ_USER")  # Modificar esto
rabbitmq_pass = os.getenv("RABBITMQ_PASS")  # Modificar esto