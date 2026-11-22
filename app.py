
import os
import socket
import mysql.connector

from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-desarrollo-cornflow")


def get_db_connection():
    """Establece una conexión con MySQL."""

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )


@app.route("/")
def inicio():

    ip_db = "No disponible"
    estado_db = "❌ Sin conexión"
    productos = []

    try:
        ip_db = socket.gethostbyname(
            os.getenv("MYSQL_HOST", "db")
        )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, codigo, nombre, descripcion, activo
            FROM productos
            ORDER BY id ASC
        """)

        productos = cursor.fetchall()

        cursor.close()
        connection.close()

        estado_db = "✅ Conexión SQL exitosa"

    except Error as error:
        print(f"Error de MySQL: {error}")
        estado_db = "❌ Error en conexión SQL"

    except Exception as error:
        print(f"Error general: {error}")
        estado_db = "❌ Error de infraestructura"

    return render_template(
        "index.html",
        estado_db=estado_db,
        ip_db=ip_db,
        productos=productos
    )


@app.route("/productos/nuevo", methods=["POST"])
def crear_producto():

    codigo = request.form.get("codigo", "").strip()
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if not codigo or not nombre:
        flash("El código y el nombre son obligatorios.", "error")
        return redirect(url_for("inicio"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO productos (codigo, nombre, descripcion)
            VALUES (%s, %s, %s)
            """,
            (codigo, nombre, descripcion or None)
        )

        connection.commit()

        flash("Producto registrado correctamente.", "success")

    except Error as error:
        print(f"Error al registrar producto: {error}")
        flash(
            "No fue posible registrar el producto. Verifica que el código no exista.",
            "error"
        )

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("inicio"))

@app.route("/productos/editar/<int:producto_id>", methods=["POST"])
def editar_producto(producto_id):

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if not nombre:
        flash("El nombre del producto es obligatorio.", "error")
        return redirect(url_for("inicio"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s, descripcion = %s
            WHERE id = %s
            """,
            (nombre, descripcion or None, producto_id)
        )

        connection.commit()

        if cursor.rowcount > 0:
            flash("Producto actualizado correctamente.", "success")
        else:
            flash("No se encontró el producto seleccionado.", "error")

    except Error as error:
        print(f"Error al editar producto: {error}")
        flash("No fue posible actualizar el producto.", "error")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("inicio"))


@app.route("/productos/desactivar/<int:producto_id>", methods=["POST"])
def desactivar_producto(producto_id):

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET activo = FALSE
            WHERE id = %s
            """,
            (producto_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            flash("Producto desactivado correctamente.", "success")
        else:
            flash("No se encontró el producto seleccionado.", "error")

    except Error as error:
        print(f"Error al desactivar producto: {error}")
        flash("No fue posible desactivar el producto.", "error")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
