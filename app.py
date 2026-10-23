"""Aplicación Flask que verifica la resolución DNS del servicio db."""

import socket

from flask import Flask

# Flask escucha en todas las interfaces para aceptar conexiones del host y de Compose.
app = Flask(__name__)


@app.route("/")
def inicio():
    """Muestra el estado de web y la IP que Docker DNS asigna al servicio db."""
    try:
        ip_db = socket.gethostbyname("db")
        estado_db = "Contenedor de base de datos encontrado."
    except socket.gaierror:
        ip_db = "No disponible"
        estado_db = "No se pudo resolver el contenedor de base de datos."

    return f"""
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Proyecto Integración Continua</title>
      </head>
      <body>
        <h1>Proyecto Integración Continua</h1>
        <p>El contenedor web está funcionando.</p>
        <p>{estado_db}</p>
        <p>IP resuelta del contenedor db: {ip_db}</p>
      </body>
    </html>
    """


if __name__ == "__main__":
    # El puerto coincide con el expuesto por Docker y publicado por Compose.
    app.run(host="0.0.0.0", port=5000)