import modin.pandas as mpd
import os
import psycopg2

'''
los datos se van acumulando en tiempo real en los csv's
el objetivo de este preprocesamiento es que en un momento dado se pasen los datos actuales limpiados y procesados 
para su visualización y para la construcción del llm
para esto los datos procesados estarán disponibles en tablas de postgresql
'''
def preprocesar():
    file_paths = ['../Crypto-Realtime/crypto_data/ADA.csv','../Crypto-Realtime/crypto_data/BNB.csv',
                  '../Crypto-Realtime/crypto_data/BTC.csv','../Crypto-Realtime/crypto_data/DOGE.csv',
                  '../Crypto-Realtime/crypto_data/ETH.csv','../Crypto-Realtime/crypto_data/SOL.csv',
                  '../Crypto-Realtime/crypto_data/STETH.csv','../Crypto-Realtime/crypto_data/USDC.csv',
                  '../Crypto-Realtime/crypto_data/USDT.csv','../Crypto-Realtime/crypto_data/XRP.csv']
    for file_path in file_paths:
        nombre = file_path.split('/')[-1].split('.')[0]
        df = mpd.read_csv(file_path)
        # aquí se pueden perder los datos que se inserten después de la carga y antes del remove
        os.remove(file_path) # kafka creará de nuevo el archivo con nuevos datos
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
        # cambiar contraseña
        conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="j73987927j", 
            host="localhost", 
            port="5432"
            )
        cursor = conn.cursor()
        # current_price, market_cap, total_volume, ath y atl son monetarios
        # circulating_supply y total_supply son cantidades
        # price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency 
        # y relative_market_cap son porcentajes
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {nombre} (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100),
                       symbol VARCHAR(10),
                       current_price NUMERIC(20, 4),
                       market_cap NUMERIC(20),
                       total_volume NUMERIC(20),
                       circulating_supply NUMERIC(20),
                       total_supply NUMERIC(20),
                       ath NUMERIC(20, 4),
                       atl NUMERIC(20, 4),
                       price_change_percentage_1h_in_currency NUMERIC(10, 4),
                       price_change_percentage_24h_in_currency NUMERIC(10, 4),
                       price_change_percentage_7d_in_currency NUMERIC(10, 4),
                       timestamp TIMESTAMP,
                       relative_market_cap NUMERIC(6, 4));
        """)
        conn.commit()
        for _, row in df.iterrows():
            cursor.execute(f"""
                           INSERT INTO {nombre} (
                           name, symbol, current_price, market_cap, total_volume, circulating_supply, 
                           total_supply, ath, atl, price_change_percentage_1h_in_currency, 
                           price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency, timestamp,
                           relative_market_cap 
                           ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                           """, (row["name"], row["symbol"], float(row["current_price"]), row["market_cap"], row["total_volume"], 
                                 row["circulating_supply"], row["total_supply"], float(row["ath"]), float(row["atl"]), 
                                 float(row["price_change_percentage_1h_in_currency"]), float(row["price_change_percentage_24h_in_currency"]), 
                                 float(row["price_change_percentage_7d_in_currency"]), row["timestamp"], row["relative_market_cap"])
            )
            conn.commit()
    cursor.close()
    conn.close()

# if __name__ == '__main__':
#     preprocesar()
