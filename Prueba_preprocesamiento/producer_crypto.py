import os
from confluent_kafka import Producer
import json
import requests
from time import sleep
from datetime import datetime

# Kafka Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Address of the Kafka broker
    'client.id': 'crypto-producer'
}

# Create a Producer instance
producer = Producer(conf)

# Function to retrieve the top 10 cryptocurrencies
def get_top_10_crypto_data():
    gecko_url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '1h,24h,7d'
    }
    
    response = requests.get(gecko_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data from CoinGecko API")
        return []


# Function to send cryptocurrency data to Kafka
def send_crypto_data_to_kafka(data):
    for coin in data:
        name = coin['name']
        symbol = coin['symbol'].upper()
        coin_data = {
            'name': name,
            'symbol': symbol,
            'current_price': coin['current_price'],
            'market_cap': coin['market_cap'],
            'total_volume': coin['total_volume'],
            'circulating_supply': coin['circulating_supply'],
            'total_supply': coin['total_supply'],
            'ath': coin['ath'],
            'atl': coin['atl'],
            'price_change_percentage_1h_in_currency': coin['price_change_percentage_1h_in_currency'],
            'price_change_percentage_24h_in_currency': coin['price_change_percentage_24h_in_currency'],
            'price_change_percentage_7d_in_currency': coin['price_change_percentage_7d_in_currency'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Send data to Kafka
        topic = 'crypto-bigdata-utec-1'  # Topic name
        key = symbol  # Use the symbol as the key
        value = json.dumps(coin_data)
        producer.produce(topic, key=key, value=value)
        print(f"Sent data for {name} ({symbol}) to Kafka")
    # Flush the producer to ensure all messages are sent
    producer.flush()

# Main loop
if __name__ == "__main__":
    while True:
        crypto_data = get_top_10_crypto_data()
        if crypto_data:
            send_crypto_data_to_kafka(crypto_data)
        sleep(15)  # Wait for 15 seconds before fetching data again
