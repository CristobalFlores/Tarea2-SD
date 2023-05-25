import json 
import sys
import time 
import matplotlib.pyplot as plt
from kafka import KafkaConsumer
from threading import *
from datetime import datetime

def plot_data():
    global latencias
    avr = sum(latencias)/len(latencias)

    plt.figure(figsize=(10, 6))
    plt.plot(latencias)
    plt.axhline(y=avr, color = 'r')
    plt.xlabel('Mensaje')
    plt.ylabel('Latencia (Segundos)')
    plt.title('Latencia de mensajes - Consumidor')

    plt.tight_layout()
    plt.show()

def consumer_thread (name , tema):

    print('inicio consumer: ' + str(name))
    
    if __name__ == '__main__':
        consumer = KafkaConsumer(
            str(tema),
            bootstrap_servers='localhost:9092',
        )
        
        for message in consumer:

            msg = json.loads(message.value)
            now = datetime.now()
        
            then = datetime.strptime((str(msg['enviado'])), '%Y-%m-%d %H:%M:%S.%f')

            delta = now.timestamp() - then.timestamp()
            global latencias
            latencias.append(delta)
            global mensajes_total 
            mensajes_total = mensajes_total+1

            print('====================================================== \n' +
                  'Consumer  '+str(name)+' recibio el mensaje de producer ' + str(msg['id']) + '\n' +
                  'N° msg   :' + str(mensajes_total) + '\n' +
                  'Tema     :' + str(tema) +  '\n' + 
                  'mensaje  :' + str(msg['temperatura']) + '\n' +
                  'envio    :' + str(msg['enviado']) + '\n' + 
                  'recibido :' + str(now) + '\n' +
                  'tiempo   :' + str(delta) + '\n' +
                  '====================================================== \n')
            
            if mensajes_total > 10000:
                global flag
                flag = 0                    
                sys.exit()


if __name__ == '__main__':

    global flag
    flag = 1
    global latencias
    latencias = []
    global mensajes_total 
    mensajes_total = 0
    inicio = datetime.now()

    P1 = Thread(target = consumer_thread, args= ['1' , 'Tema_1'])
    P2 = Thread(target = consumer_thread, args= ['2' , 'Tema_2'])      
    P3 = Thread(target = consumer_thread, args= ['3' , 'Tema_3'])     
    P4 = Thread(target = consumer_thread, args= ['4' , 'Tema_4'])
    P5 = Thread(target = consumer_thread, args= ['5' , 'Tema_5'])
    P1.start()
    P2.start()
    P3.start()  
    P4.start()  
    P5.start()      
    
    while flag == 1:
        time.sleep (1)

    fin = datetime.now()
    ttotal = fin.timestamp() - inicio.timestamp()
    print('10000 mensajes recibidos \n' +
          'tiempo inicio :' + str(inicio) + '\n' +
          'tiempo final  :' + str(fin) + '\n' +
          'tiempo total  :' + str(ttotal))


    plot_data()

    