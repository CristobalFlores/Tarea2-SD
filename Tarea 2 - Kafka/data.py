import random 
import string 
from datetime import datetime

temp = list(range(0, 100))

def gen_mensaje ( id ) -> dict:

    random_temp = random.choice(temp)

    return {
        'enviado' : str(datetime.now()),
        'temperatura': random_temp,
        'id' : id
    }

def rng_tema ():
    temas = ['Tema_1','Tema_2','Tema_3','Tema_4','Tema_5']
    tema = random.choice(temas)
    return (tema)

