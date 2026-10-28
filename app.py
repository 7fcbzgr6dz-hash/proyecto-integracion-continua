import socket

from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():

    try:
        ip_db = socket.gethostbyname("db")
        estado_db = "✅ Conectada"

    except socket.gaierror:
        ip_db = "No disponible"
        estado_db = "❌ Error de conexión"

    return f"""
    <!DOCTYPE html>
    <html lang="es">

    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>CornFlow Planner</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 20px;
            }}

            .header {{
                background: #0f4c81;
                color: white;
                padding: 25px;
                border-radius: 10px;
            }}

            .card {{
                background: white;
                margin-top: 20px;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
            }}

            ul {{
                line-height: 1.8;
            }}

            h1 {{
                margin: 0;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🌽 CornFlow Planner</h1>

            <h3>
            Sistema de Planeación y Gestión Operativa
            para Refinería de Jarabes de Maíz
            </h3>

        </div>

        <div class="card">

            <h2>Capacidad Instalada</h2>

            <p><strong>350 Toneladas por Turno</strong></p>

        </div>

        <div class="card">

            <h2>Referencias Activas</h2>

            <ul>
                <li>SM</li>
                <li>STS</li>
                <li>HMCS</li>
                <li>M-1720</li>
                <li>M-1440</li>
                <li>M-SWEET</li>
            </ul>

        </div>

        <div class="card">

            <h2>Estado de Infraestructura</h2>

            <p>🌐 Aplicación Web: ✅ Activa</p>
            <p>🗄️ Base de Datos: {estado_db}</p>
            <p>📍 IP Base de Datos: {ip_db}</p>

        </div>

        <div class="card">

            <h2>Próximos Módulos</h2>

            <ul>
                <li>Planeación Semanal</li>
                <li>Programación de Producción</li>
                <li>Control de Inventarios</li>
                <li>Capacidad de Planta</li>
                <li>Cumplimiento de Demanda</li>
                <li>Programación de Despachos</li>
            </ul>

        </div>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)