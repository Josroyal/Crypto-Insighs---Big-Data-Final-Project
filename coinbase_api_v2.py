import requests

gecko_url = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': 'false'
}

response = requests.get(gecko_url, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data from CoinGecko API")
    data = []

coinbase_url = 'https://api.coinbase.com/v2/currencies'
coinbase_response = requests.get(coinbase_url)
if coinbase_response.status_code == 200:
    coinbase_data = coinbase_response.json()
    supported_currencies = [currency['id'] for currency in coinbase_data['data']]
else:
    print("Failed to retrieve supported currencies from Coinbase")
    supported_currencies = []

for coin in data:
    name = coin['name']
    symbol = coin['symbol'].upper()

    symbol_mapping = {
        'MIOTA': 'IOTA',
    }
    symbol = symbol_mapping.get(symbol, symbol)

    if symbol in supported_currencies:
        price_url = f'https://api.coinbase.com/v2/prices/{symbol}-USD/spot'
        price_response = requests.get(price_url)

        if price_response.status_code == 200:
            price_data = price_response.json()
            amount = price_data['data']['amount']
            print(f"{name} ({symbol}): ${amount} (Price from Coinbase)")
        else:
            print(f"Failed to retrieve price for {name} ({symbol}) from Coinbase")
    else:
        price = coin['current_price']
        print(f"{name} ({symbol}): ${price} (Price from CoinGecko)")
