# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código y carpetas
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5001

# Define el comando para ejecutar la aplicación
CMD ["python", "app.py"]