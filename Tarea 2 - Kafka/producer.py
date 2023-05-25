import time 
import json 
import random 
from datetime import datetime
from data import gen_mensaje
from data import rng_tema
from kafka import KafkaProducer
from threading import *

def producer_thread (name , timesl):

    print('inicio producer: ' + str(name))

    slp = timesl
    id = name
    def serializer(message):
        return json.dumps(message).encode('utf-8')

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )
    
    if __name__ == '__main__':
        while True:

            tema = rng_tema()
            mensaje = gen_mensaje(id)
            
            print('hilo ' + str(id) +' envia el mensaje \n' +
                  'tema: ' + str(tema))
            producer.send(tema, mensaje)

            time.sleep(timesl)

if __name__ == '__main__':

    T1 = Thread(target = producer_thread, args= ['1' , random.randint(0,1)])
    T2 = Thread(target = producer_thread, args= ['2' , random.randint(0,1)])      
    T3 = Thread(target = producer_thread, args= ['3' , random.randint(0,1)])  
    T4 = Thread(target = producer_thread, args= ['4' , random.randint(0,1)])  
    T5 = Thread(target = producer_thread, args= ['5' , random.randint(0,1)])     
    T1.start()
    T2.start()
    T3.start()
    T4.start()
    T5.start()