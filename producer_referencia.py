import os
from confluent_kafka import Producer
import pandas as pd
from time import sleep
import json
import random
from datetime import datetime

os.environ['KAFKAJS_NO_PARTITIONER_WARNING'] = '1' # Para evitar un warning

# Configuración del productor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'client.id': 'my-producer'
}

# Crear una instancia del productor
producer = Producer(conf)

# Función de callback para manejar eventos de envío
'''
def delivery_report(err, msg):
    if err is not None:
        print(f"Error en el envío del mensaje: {err}")
    else:
        print(f"Mensaje enviado a {msg.topic()} [{msg.partition()}] @ {msg.offset()}")
'''

def generate_sensor_event():
    sensor_id = random.randint(1, 10)
    temperature = round(random.uniform(-10, 35), 5)
    humidity = round(random.uniform(0, 100), 5)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        'sensor_id': sensor_id,
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': timestamp
    }
    
def get_partition(sensor_id):
    if sensor_id >= 1 and sensor_id <= 5:
        return 0
    elif sensor_id >= 6 and sensor_id <= 10:
        return 1   
    
# Enviar un mensaje
while True:
    event = generate_sensor_event()
    partition = get_partition(event['sensor_id'])
    producer.produce('sensor-events', key=str(event['sensor_id']), value=json.dumps(event), partition=partition)
    # Mensaje de confirmación estructura: JOSUE: Mensaje enviado a la partición n: {datos del sensor}
    print(f"JOSUE ARBULU: Mensaje enviado a la partición {partition}: {event}")
    producer.flush()
    sleep(1)