import psycopg2

def insights():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="j73987927j", 
        host="localhost", 
        port="5432"
    )
    cursor = conn.cursor()
    # vista para las criptomonedas más volátiles en un momento dado
    cursor.execute('''create view top_volatiles as (
                   SELECT name, price_change_percentage_24h_in_currency, timestamp
                   FROM criptomonedas
                   ORDER BY price_change_percentage_24h_in_currency DESC
                   LIMIT 20
                   ) 
                   ''')
    # vista para los precios actuales promedios de cada criptomoneda para el rango de tiempo
    cursor.execute('''create view promedio_precio as (
                   SELECT symbol, AVG(current_price) AS avg_price
                   FROM criptomonedas
                   GROUP BY symbol
                   ORDER BY avg_price DESC
                   ) 
                   ''')
    # vista para los precios actuales promedios de cada criptomoneda cada dia
    cursor.execute('''create view precios_promedio_por_dia as (
                   SELECT symbol, DATE(timestamp) AS day, AVG(current_price) AS avg_daily_price
                   FROM criptomonedas
                   GROUP BY symbol, day
                   ORDER BY symbol, day
                   )
                   ''')
    # vista para el top de criptomonedas según el capital de mercado
    cursor.execute('''create view top_capital_mercado as (
                   SELECT name, symbol, market_cap, timestamp
                   FROM criptomonedas
                   ORDER BY market_cap DESC
                   ) 
                   ''')
    conn.commit()
    cursor.close()
    conn.close()

insights()