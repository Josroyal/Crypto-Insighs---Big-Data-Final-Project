from confluent_kafka import Consumer, KafkaException
import json
import pandas as pd

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
    'group.id': 'my-consumer-group',        # ID del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Comenzar desde el inicio de los mensajes
}

# Crear una instancia del consumidor
consumer = Consumer(conf)

# Suscribirse al topic
consumer.subscribe(['sensor-events'])

# Leer mensajes del topic
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Tiempo de espera para recibir mensajes
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        
        sensor_event = json.loads(msg.value().decode('utf-8'))
        sensor_id = sensor_event['sensor_id']
        temperature = sensor_event['temperature']
        timestamp = sensor_event['timestamp']
        
        with open('PC/sensor_events.csv', 'a') as f:
            f.write(f"{sensor_id},{temperature},{timestamp}\n")
        
        if temperature > 30:
            print(f"Josue: Temperatura alta detectada: {temperature}°C en el sensor {sensor_id} a las {timestamp}")
            
            # escribir en warnings.csv
            with open('PC/sensor_warnings.csv', 'a') as f:
                f.write(f"{sensor_id},{temperature},{timestamp}\n")


except KeyboardInterrupt:
    pass
finally:
    consumer.close()
