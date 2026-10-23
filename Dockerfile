# Imagen base ligera con la versión de Python solicitada para el proyecto.
FROM python:3.11-slim

# Mantiene los archivos de la aplicación en una ubicación predecible.
WORKDIR /app

# Instala dependencias antes de copiar el código para aprovechar la caché de capas.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia la aplicación y ejecuta el contenedor con un usuario sin privilegios.
COPY app.py .
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app
USER appuser

# Documenta el puerto HTTP que utiliza Flask.
EXPOSE 5000

# Inicia el servidor Flask al arrancar el contenedor.
CMD ["python", "app.py"]