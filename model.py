import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib
import os

# Crear la carpeta 'Models' si no existe
os.makedirs('Models', exist_ok=True)

# Lista de las 9 criptomonedas más populares
cryptos = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'bitcoin-cash', 'cardano', 'polkadot', 'stellar', 'dogecoin']

def train_model(crypto):
    # Cargar los datos desde el archivo CSV correspondiente dentro de la carpeta 'Data'
    df = pd.read_csv(f'Data/{crypto}_historical_data.csv')

    # Crear nuevas columnas para representar el día, mes, y año a partir del timestamp
    df['day'] = pd.to_datetime(df['timestamp']).dt.day
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['year'] = pd.to_datetime(df['timestamp']).dt.year

    # Variables independientes (X) y dependientes (y)
    X = df[['day', 'month', 'year']]
    y = df['price']

    # Separar los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar un modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    accuracy = r2_score(y_test, y_pred)
    print(f'Precisión del modelo para {crypto}: {accuracy}')

    # Guardar el modelo entrenado en un archivo .pkl dentro de la carpeta 'Models'
    model_filename = f'Models/{crypto}_model.pkl'
    joblib.dump(model, model_filename)
    print(f'Modelo guardado como {model_filename}')

# Entrenar y guardar un modelo para cada criptomoneda
for crypto in cryptos:
    train_model(crypto)