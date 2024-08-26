import requests
import pandas as pd
from datetime import datetime
import time
import os

# Crear la carpeta 'Data' si no existe
os.makedirs('Data', exist_ok=True)

def get_crypto_data(crypto_id, vs_currency='usd', days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,
    }
    response = requests.get(url, params=params)
    
    # Imprimir la respuesta completa de la API si ocurre un error
    if response.status_code != 200:
        print(f"Error al obtener datos para {crypto_id}: {response.json()}")
        return None

    data = response.json()
    prices = data.get('prices', None)
    
    if prices is None:
        print(f"Error: La clave 'prices' no se encuentra en la respuesta de la API para {crypto_id}.")
        return None

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Lista de las 9 criptomonedas más populares
cryptos = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'bitcoin-cash', 'cardano', 'polkadot', 'stellar', 'dogecoin']

# Período para el cual queremos los datos (por ejemplo, los últimos 365 días)
days = 365

# Recolectar datos para cada criptomoneda y guardarlos en archivos CSV dentro de la carpeta 'Data'
for crypto in cryptos:
    df = get_crypto_data(crypto, days=days)
    if df is not None:
        df.to_csv(f'Data/{crypto}_historical_data.csv', index=False)
        print(f'Datos guardados para {crypto}.')
        print(df.head())
    else:
        print(f'No se pudieron obtener datos para {crypto}')
    # Añadir un retraso de 1 segundo entre solicitudes
    time.sleep(1)