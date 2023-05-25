# Tarea2-Sistemas-distribuidos <br/><br/>
Segunda Tarea de sistemas distribuidos <br/>
Cristóbal Flores Monroy || 19.954.317-2 || cristobal.flores1@mail.udp.cl <br/>
Ignacio Eduardo Boettcher Hermosilla || 19.743.304-3 || ignacio.boettcher@mail.udp.cl <br/> <br/>

link video kafka : https://youtu.be/Fx6ntp580e8
link video RabbitMQ : https://youtu.be/IktMlTjOGrc <br/>

======================================================================== <br/><br/>

Orden de ejecucion del codigo Kafka: <br/> <br/>

1.- ingresar a la ruta '/Sis distribuidos/Docker' <br/>
2.- Instanciar Kafka y Zookeeper en un docker mediante ' -f \docker-compose.yml up -d ' <br/>
3.- Ingresar a la ruta '/Sis distribuidos' <br/>
4.- Ejecutar 'consumer.py' <br/>
5.- Ejecutar 'Producer.py' <br/>
Importante recordar cerrar producer por que no cuenta con una instruccion de finalizacion <br/>
<br/>

======================================================================== <br/><br/>

Orden de ejecucion del codigo RabbitMQ: <br/> <br/>

En este archivo docker-compose.yml, estamos definiendo un servicio llamado rabbitmq que se construirá a partir del Dockerfile en el mismo <br/>
directorio (eso es lo que significa el . en la línea de build). También estamos mapeando los puertos 5672 y 15672 de RabbitMQ a los mismos puertos en tu máquina local.<br/><br/>

Puedes construir y ejecutar tu contenedor utilizando Docker Compose con el siguiente comando:<br/><br/>

---------------------------<br/><br/
$ docker-compose build <br/>
$ docker-compose up  ##Esto levantara todo los servicios en una misma terminal (no recomendable) <br/>
Despues levantamos cada servicio en una terminal distinta <br/> <br/>

$ docker-compose up rabbitmq <br/>
Una vez tengamos corriendo el contenedor con el servidor de RabbitMQ meternos a <br/>
http://localhost:15672 <br/><br/>

Esta parte fue de prueba para los contenedores <br/>

########################################### <br/>

$ docker-compose up productor   ## (CONTENEDORES) esto correra el productor con los valores por defecto 10 dispositivos 5 seg  <br/>
$ docker-compose up consumidor  ## (CONTENEDORES) esto correra el consumidor con los valores por defecto 1 por categoria  <br/><br/>

--------------------------- <br/>
########################################## <br/>

para correr con valores propios el siguiente comando <br/>
Ejemplo: <br/>

$ python Productor-RabbitMQ.py --num_dispo 15 --delta_time 3 <br/>

$ python Consumidor-RabbitMQ.py --num_consumers 5 <br/>
Numero de consumers por categoria EN este ejemplo de 5 en total serian 20 consumidores en total <br/>
EL NUMERO DE CONSUMIDORES TIENE QUE SER MAYOR O IGUAL A 5 <br/>


