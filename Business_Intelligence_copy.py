import psycopg2
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime

st.title("Dashboard Criptomonedas")

def connect_to_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="j73987927j",
        host="localhost",
        port="5432"
    )

@st.cache_data(ttl=10)
def load_crypto_data():
    conn = connect_to_db()
    crypto_data = {}
    try:
        query = "SELECT * FROM criptomonedas"
        df = pd.read_sql(query, conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        for symbol in df['symbol'].unique():
            crypto_data[symbol] = df[df['symbol'] == symbol]
    finally:
        conn.close()
    return crypto_data

def create_graph(data, crypto_name):
    if 'timestamp' in data.columns and 'current_price' in data.columns:
        return go.Scatter(
            x=data['timestamp'],
            y=data['current_price'],
            mode='lines',
            name=crypto_name
        )
    else:
        return None

crypto_data = load_crypto_data()

st.header("Criptomonedas con el pasar del tiempo")
cryptos_to_plot = st.multiselect(
    "Selecciona criptomoneda:", 
    list(crypto_data.keys()),
    key="multiselect_cryptos"
)

fig1 = go.Figure()
for crypto_name in cryptos_to_plot:
    if crypto_name in crypto_data:
        graph = create_graph(crypto_data[crypto_name], crypto_name)
        if graph:
            fig1.add_trace(graph)
fig1.update_layout(
    title="Criptomonedas con el pasar del tiempo",
    xaxis_title="Tiempo",
    yaxis_title="Precio (USD)",
    template="plotly_dark"
)
st.plotly_chart(fig1)

st.header("Market Cap vs Volumen Total")
crypto_for_market_volume = st.selectbox(
    "Seleccionar Criptomoneda", 
    list(crypto_data.keys()), 
    key="selectbox_market_volume"
)

fig5 = go.Figure()
if crypto_for_market_volume:
    data = crypto_data[crypto_for_market_volume]
    if 'market_cap' in data.columns and 'total_volume' in data.columns:
        latest_row = data.iloc[-1]
        fig5.add_trace(go.Bar(
            x=['Market Cap', 'Total Volume'],
            y=[latest_row['market_cap'], latest_row['total_volume']],
            name=crypto_for_market_volume
        ))
        fig5.update_layout(
            title=f"Market Cap vs Volumen Total ({crypto_for_market_volume})",
            yaxis_title="Valor",
            template="plotly_dark"
        )
st.plotly_chart(fig5)

st.header("El porcentaje de cambio de precio en 24 horas")
fig9 = go.Figure()
for crypto_name, data in crypto_data.items():
    if 'price_change_percentage_24h_in_currency' in data.columns:
        latest_change = data['price_change_percentage_24h_in_currency'].iloc[-1]
        fig9.add_trace(go.Bar(
            x=[crypto_name],
            y=[latest_change],
            name=crypto_name,
            text=f"{latest_change:.2f}%",
            textposition='outside'
        ))
fig9.update_layout(
    title="El porcentaje de cambio de precio en 24 horas",
    xaxis_title="Criptomoneda",
    yaxis_title="Cambio de precio (%)",
    template="plotly_dark",
    showlegend=False
)
st.plotly_chart(fig9)

st.header("Todas los precios de las criptomonedas juntas")
fig4 = go.Figure()
for crypto_name, data in crypto_data.items():
    graph = create_graph(data, crypto_name)
    if graph:
        fig4.add_trace(graph)
fig4.update_layout(
    title="Todas las criptomonedas juntas",
    xaxis_title="Tiempo",
    yaxis_title="Precio (USD)",
    template="plotly_dark"
)
st.plotly_chart(fig4)


st.header("Últimas Noticias")

@st.cache_data(ttl=10)
def load_news_data():
    news_df = pd.read_csv("path_to_your_news_file/news.csv")
    return news_df

news_df = load_news_data()
st.table(news_df[['title', 'author']])


st.text(f"Actualizado por ultima vez: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
