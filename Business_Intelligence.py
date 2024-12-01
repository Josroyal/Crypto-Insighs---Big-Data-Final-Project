import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime


FOLDER_PATH = "Crypto-Realtime/crypto_data"

def load_crypto_data(folder_path):
    crypto_data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            crypto_name = file_name.split('.')[0].upper()
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            crypto_data[crypto_name] = df
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
        st.error(f"El archivo {crypto_name} le falta las columnas timestamp o current_price")
        return None


st.title("Data de Criptomonedas en tiempo real")

crypto_data = load_crypto_data(FOLDER_PATH)

cryptos_to_plot = st.multiselect("Selección de Criptomoneda", list(crypto_data.keys()))

fig = go.Figure()

for crypto_name in cryptos_to_plot:
    if crypto_name in crypto_data:
        graph = create_graph(crypto_data[crypto_name], crypto_name)
        if graph:
            fig.add_trace(graph)

fig.update_layout(
    title="Precios de Criptomonedas en tiempo real",
    xaxis_title="Tiempo",
    yaxis_title="Precio (USD)",
    template="plotly_dark"
)

st.plotly_chart(fig)

st.text(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("The data will automatically update when the CSV files are modified.")
