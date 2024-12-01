from confluent_kafka import Consumer, KafkaException
import json
import pandas as pd
import os

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Address of the Kafka broker
    'group.id': 'crypto-consumer-group',    # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start from the beginning of the topic
}

# Create a Consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['crypto-bigdata-utec-1'])

# Directory to save CSV files
output_dir = 'crypto_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read messages from the topic
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Wait time for receiving messages
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        
        coin_data = json.loads(msg.value().decode('utf-8'))
        symbol = coin_data['symbol']
        # Create a DataFrame from the coin data
        df = pd.DataFrame([coin_data])
        
        # Define the CSV file path
        csv_file = os.path.join(output_dir, f'{symbol}.csv')
        
        # Append data to the CSV file
        if not os.path.exists(csv_file):
            # If file does not exist, write headers
            df.to_csv(csv_file, mode='w', index=False)
        else:
            # If file exists, append without headers
            df.to_csv(csv_file, mode='a', index=False, header=False)
        
        print(f"Data for {coin_data['name']} ({symbol}) saved to {csv_file}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
