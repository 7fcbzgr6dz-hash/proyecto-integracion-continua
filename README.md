# Proyecto Integración Continua

## Objetivo

Desplegar una aplicación web hecha con Python y Flask junto a una base de datos MySQL, usando Docker Compose para construir, iniciar y conectar ambos contenedores.

La página comprueba la resolución DNS del servicio `db` con `socket.gethostbyname("db")`. Esta práctica verifica que los contenedores comparten la red de Compose; no realiza una consulta ni una conexión SQL.

## Arquitectura

- **web**: imagen construida desde el `Dockerfile`, basada en Python 3.11. Flask escucha en el puerto 5000.
- **db**: imagen oficial `mysql:8.0`, inicializada con la base `universidad`.
- **Red**: Compose crea automáticamente una red privada; el servicio web encuentra MySQL por el nombre DNS `db`.
- **Persistencia**: el volumen `mysql_data` conserva los datos de MySQL al recrear los contenedores.
- **Arranque**: `web` depende del estado saludable de `db`, determinado mediante un healthcheck de MySQL.

## Requisitos previos

- Docker Desktop (o Docker Engine) con el complemento Docker Compose.
- Puertos 5000 y 3306 disponibles en el equipo.

## Cómo ejecutar

Desde la carpeta del proyecto, construye e inicia los servicios:

```bash
docker compose up --build
```

Abre [http://localhost:5000](http://localhost:5000). La página muestra el título del proyecto, el estado del contenedor web, si se resolvió el servicio de base de datos y la dirección IP devuelta por Docker DNS.

Para detener los servicios sin eliminar los datos persistidos:

```bash
docker compose down
```

Para eliminar también los datos de MySQL:

```bash
docker compose down -v
```

## Evidencias para la entrega

1. Captura de la salida de `docker compose ps` donde se vean los servicios `web` y `db` activos.
2. Captura del navegador en `http://localhost:5000` con los mensajes y la IP resuelta.
3. Captura de `docker compose logs web db` como evidencia del inicio de ambos servicios.
4. Captura de la sección de redes o del comando `docker network ls` que muestre la red creada por Compose.

## Archivos del proyecto

- `app.py`: ruta Flask y comprobación de DNS.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: construcción de la imagen web.
- `docker-compose.yml`: servicios, puertos, healthcheck y volumen.
- `.gitignore`: archivos locales excluidos de Git.

## Nota de seguridad

Las credenciales solicitadas (`root123`) son únicamente para esta práctica. No se deben reutilizar en producción; allí se recomienda administrar secretos fuera del archivo Compose y utilizar un servidor WSGI de producción en lugar del servidor de desarrollo de Flask.