# CornFlow Planner

Aplicación web para la gestión y consulta de productos de CornFlow Planner, desarrollada como proyecto académico de Integración Continua.

Este proyecto utiliza **Python, Flask, MySQL, Docker y Jenkins**.

---

# 1. ¿Qué hace este proyecto?

CornFlow Planner es una aplicación web que permite:

- Consultar los productos registrados.
- Registrar nuevos productos.
- Editar la información de los productos.
- Desactivar productos sin eliminarlos físicamente de la base de datos.
- Almacenar la información en una base de datos MySQL.
- Ejecutar pruebas automatizadas mediante Pytest.
- Integrar un pipeline de Integración Continua utilizando Jenkins.

# 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje de programación |
| Flask | Framework para desarrollar la aplicación web |
| MySQL 8 | Base de datos |
| HTML / CSS / JavaScript | Interfaz de usuario |
| Docker | Ejecución de los servicios mediante contenedores |
| Docker Compose | Administración de los contenedores |
| Pytest | Ejecución de pruebas automatizadas |
| Jenkins | Automatización del proceso de Integración Continua |
| Git / GitHub | Control de versiones y almacenamiento del código |

# 3. Requisitos previos

Antes de ejecutar el proyecto, debes tener instalados los siguientes programas.

## 3.1. Instalar Docker Desktop

Docker permite ejecutar la aplicación y la base de datos sin instalar Python o MySQL manualmente en tu computador.

1. Ingresa a la página oficial:

   https://www.docker.com/products/docker-desktop/

2. Descarga Docker Desktop para Windows.
3. Ejecuta el instalador.
4. Sigue las instrucciones de instalación.
5. Reinicia el computador si el instalador lo solicita.
6. Abre Docker Desktop.
7. Espera hasta que Docker indique que está funcionando correctamente.

**Importante:** Docker Desktop debe permanecer abierto mientras utilices el proyecto.

## 3.2. Instalar Git

Git permite descargar el proyecto desde GitHub.

1. Ingresa a:

   https://git-scm.com/downloads

2. Descarga Git para Windows.
3. Ejecuta el instalador.
4. Puedes conservar las opciones predeterminadas.
5. Finaliza la instalación.

Para comprobar que Git está instalado, abre PowerShell y ejecuta:

```powershell
git --version
```

Debe aparecer una versión de Git.

# 4. Descargar el proyecto

Abre PowerShell.

Primero, dirígete a la carpeta donde deseas guardar el proyecto. Por ejemplo:

```powershell
cd Documents
```

Después, descarga el repositorio:

```powershell
git clone https://github.com/7fcbzgr6dz-hash/proyecto-integracion-continua.git
```

Ingresa a la carpeta del proyecto:

```powershell
cd proyecto-integracion-continua
```

A partir de este momento, todos los comandos de este documento deben ejecutarse desde esta carpeta, salvo que se indique lo contrario.

# 5. Configurar las variables de entorno

El proyecto utiliza un archivo `.env` para configurar la conexión con MySQL.

Este archivo contiene los datos necesarios para que la aplicación pueda comunicarse con la base de datos.

## 5.1. Crear el archivo de configuración

En PowerShell ejecuta:

```powershell
Copy-Item .env.example .env
```

Este comando crea una copia del archivo de ejemplo.

## 5.2. Revisar el archivo `.env`

Abre el proyecto en Visual Studio Code o utiliza cualquier editor de texto.

Busca el archivo `.env` y verifica que tenga las siguientes variables:

```env
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_DATABASE=universidad
MYSQL_USER=cornflow_app
MYSQL_PASSWORD=CornFlow_Dev_2026!
MYSQL_ROOT_PASSWORD=root123
```

Reemplaza los valores de las contraseñas por los valores que correspondan a tu configuración.

**Importante:**

- `MYSQL_HOST` debe conservar el valor `db`, porque es el nombre del servicio de MySQL dentro de Docker Compose.
- `MYSQL_PORT` debe conservar el valor `3306`.
- El usuario, las contraseñas y la base de datos deben coincidir con la configuración utilizada en `docker-compose.yml`.
- No cambies los nombres de las variables.

El archivo `.env` es local y no debe subirse a GitHub.

# 6. Ejecutar el proyecto

Esta es la parte más importante.

No necesitas instalar Python, Flask ni MySQL manualmente. Docker se encargará de preparar el entorno.

## 6.1. Construir e iniciar los contenedores

Desde la carpeta principal del proyecto ejecuta:

```powershell
docker compose up -d --build
```

¿Qué hace este comando?

- `docker compose`: administra los servicios definidos en el proyecto.
- `up`: crea e inicia los contenedores.
- `-d`: ejecuta los servicios en segundo plano.
- `--build`: construye las imágenes necesarias antes de iniciar los servicios.

La primera ejecución puede tardar algunos minutos porque Docker necesita descargar las imágenes e instalar las dependencias.

## 6.2. Verificar que los contenedores estén funcionando

Ejecuta:

```powershell
docker compose ps
```

Debes encontrar los siguientes servicios:

| Servicio | Función | Puerto |
|---|---|---|
| web | Aplicación Flask | 5000 |
| db | Base de datos MySQL | 3306 |
| jenkins | Servidor de Integración Continua | 8080 y 50000 |

Los servicios deben aparecer en estado `Up`, `Running` o equivalente. La base de datos debe llegar a estado `healthy`.

Si la base de datos todavía aparece como `starting`, espera unos segundos y vuelve a ejecutar el comando.

## 6.3. Abrir la aplicación

Cuando los contenedores estén funcionando, abre tu navegador e ingresa a:

**Aplicación CornFlow Planner:**

http://localhost:5000

¡Listo! La aplicación debería estar funcionando.

# 7. Base de datos MySQL

El proyecto utiliza MySQL 8 para almacenar los productos.

La configuración de la base de datos se encuentra en:

```text
database/
└── schema.sql
```

Este archivo contiene las instrucciones SQL para crear la tabla `productos` y registrar los productos iniciales.

## 7.1. Tabla productos

La tabla contiene los siguientes campos:

| Campo | Descripción |
|---|---|
| id | Identificador único del producto |
| codigo | Código único del producto |
| nombre | Nombre del producto |
| descripcion | Descripción del producto |
| activo | Indica si el producto está activo |
| created_at | Fecha de creación del registro |

## 7.2. Productos iniciales

Al inicializar una base de datos nueva se insertan los siguientes productos:

- SM
- STS
- HMCS
- M-1720
- M-1440
- M-SWEET

## 7.3. ¿Cuándo se ejecuta el archivo schema.sql?

Docker monta el archivo `database/schema.sql` en el directorio de inicialización de MySQL.

MySQL ejecuta automáticamente estos scripts cuando inicializa un directorio de datos vacío.

**Importante:** Si la base de datos ya fue creada anteriormente, modificar `schema.sql` no significa que MySQL volverá a ejecutar automáticamente todo el archivo.

El proyecto utiliza un volumen persistente para conservar los datos.

# 8. Ejecutar las pruebas automatizadas

El proyecto utiliza Pytest para verificar el funcionamiento de las operaciones principales de la aplicación.

Las