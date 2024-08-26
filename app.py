from flask import Flask, render_template, request
import joblib
import pandas as pd
from datetime import datetime
import requests

app = Flask(__name__)

# Lista de las 9 criptomonedas más populares
cryptos = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'bitcoin-cash', 'cardano', 'polkadot', 'stellar', 'dogecoin']

def load_model(crypto):
    try:
        model_filename = f'Models/{crypto}_model.pkl'
        model = joblib.load(model_filename)
        return model
    except FileNotFoundError:
        return None

def predict_price(model, date):
    # Convertir la fecha a componentes día, mes y año
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year
    
    # Crear DataFrame para la fecha seleccionada
    data = pd.DataFrame([[day, month, year]], columns=['day', 'month', 'year'])
    
    # Realizar la predicción
    prediction = model.predict(data)[0]
    return prediction, day, month, year

def get_current_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': crypto,
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get(crypto, {}).get('usd', 'No disponible')
    return 'No disponible'

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_crypto = None
    predicted_price = None
    current_price = None
    day = None
    month = None
    year = None

    if request.method == 'POST':
        selected_crypto = request.form.get('crypto')
        date = request.form.get('date')
        
        if selected_crypto and date:
            model = load_model(selected_crypto)
            if model:
                predicted_price, day, month, year = predict_price(model, date)
                current_price = get_current_price(selected_crypto)
            else:
                predicted_price = 'Modelo no disponible para la criptomoneda seleccionada.'

    return render_template('index.html', cryptos=cryptos, selected_crypto=selected_crypto, 
                           predicted_price=predicted_price, current_price=current_price, 
                           day=day, month=month, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)