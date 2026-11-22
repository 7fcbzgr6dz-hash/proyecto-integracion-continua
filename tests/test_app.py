
import pytest
from unittest.mock import patch

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_pagina_principal_responde(client):
    """Comprueba que la página principal carga correctamente."""

    with patch("app.get_db_connection") as mock_db:
        mock_connection = mock_db.return_value
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.fetchall.return_value = []

        response = client.get("/")

        assert response.status_code == 200
        assert b"CornFlow Planner" in response.data


def test_crear_producto_correctamente(client):
    """Comprueba que un producto se registra correctamente."""

    with patch("app.get_db_connection") as mock_db:
        mock_connection = mock_db.return_value
        mock_cursor = mock_connection.cursor.return_value

        response = client.post(
            "/productos/nuevo",
            data={
                "codigo": "TEST-002",
                "nombre": "Producto de prueba",
                "descripcion": "Producto creado desde una prueba automatizada"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Producto registrado correctamente." in response.data

        assert mock_cursor.execute.call_count == 2
        mock_connection.commit.assert_called_once()


def test_editar_producto_correctamente(client):
    """Comprueba que un producto se actualiza correctamente."""

    with patch("app.get_db_connection") as mock_db:
        mock_connection = mock_db.return_value
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.rowcount = 1

        response = client.post(
            "/productos/editar/1",
            data={
                "nombre": "Producto actualizado",
                "descripcion": "Descripción actualizada desde pytest"
            }
        )

        assert response.status_code == 302

        mock_cursor.execute.assert_called_once()

        consulta = mock_cursor.execute.call_args[0][0]
        parametros = mock_cursor.execute.call_args[0][1]

        assert "UPDATE productos" in consulta
        assert parametros == (
            "Producto actualizado",
            "Descripción actualizada desde pytest",
            1
        )

        mock_connection.commit.assert_called_once()


def test_desactivar_producto_correctamente(client):
    """Comprueba que un producto se desactiva correctamente."""

    with patch("app.get_db_connection") as mock_db:
        mock_connection = mock_db.return_value
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.rowcount = 1

        response = client.post("/productos/desactivar/1")

        assert response.status_code == 302

        mock_cursor.execute.assert_called_once()

        consulta = mock_cursor.execute.call_args[0][0]
        parametros = mock_cursor.execute.call_args[0][1]

        assert "UPDATE productos" in consulta
        assert "SET activo = FALSE" in consulta
        assert parametros == (1,)

        mock_connection.commit.assert_called_once()
