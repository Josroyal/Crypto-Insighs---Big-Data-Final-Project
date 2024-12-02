from confluent_kafka import Consumer, KafkaException
import json
import pandas as pd
import os
import psycopg2
import modin.pandas as mpd

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

def preprocesar(df):
    # cambiar contraseña
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="j73987927j", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
    # eliminar filas con datos vacíos en caso de haber
    df = df.dropna()
    # pasar el timestamp a datetime en caso de no estar formateado
    df['timestamp'] = mpd.to_datetime(df['timestamp'])
    # redondear variables con muchos decimales a 4 decimales
    df["price_change_percentage_1h_in_currency"] = df["price_change_percentage_1h_in_currency"].round(4)
    df["price_change_percentage_24h_in_currency"] = df["price_change_percentage_24h_in_currency"].round(4)
    df["price_change_percentage_7d_in_currency"] = df["price_change_percentage_7d_in_currency"].round(4)
    df["atl"] = df["atl"].round(4)
    # agregar el ratio entre el capital de mercado y el suministro total
    df['relative_market_cap'] = df['market_cap'] / df['total_supply'] # mientras más cerca a 1 mayor circulación con respecto al suministro
    df['relative_market_cap'] = df['relative_market_cap'].round(4)
    for _, row in df.iterrows():
        cursor.execute(f"""
                       INSERT INTO criptomonedas (
                        name, symbol, current_price, market_cap, total_volume, circulating_supply, 
                        total_supply, ath, atl, price_change_percentage_1h_in_currency, 
                        price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency, timestamp,
                        relative_market_cap 
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """, (row["name"], row["symbol"], float(row["current_price"]), row["market_cap"], row["total_volume"], 
                              row["circulating_supply"], row["total_supply"], float(row["ath"]), float(row["atl"]), 
                              float(row["price_change_percentage_1h_in_currency"]), float(row["price_change_percentage_24h_in_currency"]), 
                              float(row["price_change_percentage_7d_in_currency"]), row["timestamp"], float(row["relative_market_cap"]))
        )
        conn.commit()
    cursor.close()
    conn.close()

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
        nombre = "criptomonedas"
        preprocesar(df)
        print(f"Data for {coin_data['name']} ({symbol}) saved to {nombre}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
