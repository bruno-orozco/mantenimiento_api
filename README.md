# API de Mantenimiento de Vehículos

Esta API proporciona un sistema de gestión de órdenes de mantenimiento para vehículos. Permite la creación, lectura y gestión de órdenes de mantenimiento y vehículos mediante operaciones RESTful.

## Casos de uso soportados

- **CRUD de Órdenes de Mantenimiento**: Gestiona las órdenes de mantenimiento para cada vehículo.
- **CRUD de Vehículos**: Gestiona los vehículos registrados en el sistema.

## Arquitectura

El proyecto está diseñado siguiendo una arquitectura basada en capas, que separa las responsabilidades en diferentes módulos para una mejor organización y mantenibilidad del código:

### Directorios
- **Modelo de Datos (Models)**: Define la estructura de las tablas de la base de datos utilizando SQLAlchemy ORM.
- **Capa de Acceso a Datos (CRUD)**: Implementa las operaciones de acceso a datos utilizando SQLAlchemy para interactuar con la base de datos.
- **Capa de Negocio (Routers)**: Define las rutas de la API utilizando FastAPI, y gestiona las peticiones HTTP.
- **Esquemas (Schemas)**: Especifican la estructura y validaciones de los datos que serán recibidos o devueltos por la API.

### Configuración
- **Base de Datos (database.py)**: Utiliza PostgreSQL para almacenar los datos de los vehículos y las órdenes de mantenimiento.
- **Configuración (config.py)**: carga y obtiene variables de entorno desde un archivo .env, utilizado para configurar la conexión a una base de datos PostgreSQL.
- **Principal (main.py)**: configura y crea una API utilizando FastAPI, define rutas básicas y se asegura de que las tablas de la base de datos estén creadas al inicio de la aplicación.
 ```bash
├── app
│   ├── crud
│   ├── models
│   ├── routers
│   └── schemas
│   ├──── database.py
│   ├──── config.py
│   ├──── main.py
├── tests
│   ├──── test_maintenance.py
│   └──── test_vehicle.py
 ```

## Tecnologías utilizadas

- **Python v 3.10.11**: Es el lenguaje de programación principal utilizado en este proyecto.

- **FastAPI v 0.111.0**: Se eligió FastAPI como framework web debido a su alta velocidad y facilidad de desarrollo. Es ideal para construir APIs modernas y eficientes con soporte para tipado estático (usando Pydantic) y documentación automática (usando OpenAPI y Swagger UI).

- **PostgreSQL v 14.12**: Se eligió PostgreSQL como sistema de gestión de base de datos relacional debido a su robustez, capacidad de escalabilidad y facilidad de implementación. 

- **Docker**: Docker se utiliza para la contenerización de la aplicación. Permite empaquetar la aplicación junto con todas sus dependencias en un contenedor, lo que garantiza que la aplicación se ejecute de manera consistente en diferentes entornos.
Estas tecnologías fueron seleccionadas para asegurar un desarrollo eficiente y robusto de la aplicación.

## Instalación y Uso con Docker

1. **Clona el repositorio:**

 ```bash
 git clone https://github.com/bruno-orozco/mantenimiento_api.git
 cd mantenimiento_api
 ```

2. **Construye y ejecuta los contenedores de Docker:**

```bash
docker-compose up -d --build
```

3. **Accede a la documentación de la API:**

La API estará disponible en http://localhost:8000/docs. Aquí podrás interactuar con la API mediante Swagger UI, que proporciona una descripción de cada endpoint, parámetros de entrada y ejemplos de respuestas.

---

## Documentación de Pruebas Unitarias desarrolladas

### `test_maintenance.py`

Este archivo contiene pruebas unitarias para endpoints relacionados con órdenes de mantenimiento en la API.

### Pruebas

#### `test_create_maintenance_order`

- **Descripción**: Prueba la creación de una orden de mantenimiento.
- **Endpoints Probados**: `POST /maintenance-orders/`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los datos ingresados.
  - Los tipos de datos deben ser los esperados.

#### `test_read_maintenance_order`

- **Descripción**: Prueba la lectura de una orden de mantenimiento por su ID.
- **Endpoints Probados**: `GET /maintenance-orders/{id}`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los datos de la orden creada.
  - Los tipos de datos deben ser los esperados.

#### `test_read_maintenance_orders`

- **Descripción**: Prueba la obtención de todas las órdenes de mantenimiento.
- **Endpoints Probados**: `GET /maintenance-orders/`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista.
  - Cada orden en la lista debe tener los atributos y tipos de datos esperados.

#### `test_read_maintenance_orders_with_pagination`

- **Descripción**: Prueba la obtención de órdenes de mantenimiento con paginación.
- **Endpoints Probados**: `GET /maintenance-orders/?skip=0&limit=10`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista de longitud 10.
  - Cada orden en la lista debe tener los atributos y tipos de datos esperados.

---

### `test_vehicle.py`

Este archivo contiene pruebas unitarias para endpoints relacionados con vehículos en la API.

#### `test_create_vehicle`

- **Descripción**: Prueba la creación de un vehículo.
- **Endpoints Probados**: `POST /vehicles/`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los datos ingresados.
  - Los tipos de datos deben ser los esperados.

#### `test_create_vehicle_already_registered`

- **Descripción**: Prueba el escenario donde un vehículo ya está registrado.
- **Endpoints Probados**: `POST /vehicles/`
- **Validación**:
  - Código de estado debe ser 400.
  - La respuesta debe indicar que el vehículo ya está registrado.

#### `test_read_vehicle`

- **Descripción**: Prueba la lectura de un vehículo por su ID.
- **Endpoints Probados**: `GET /vehicles/{id}`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los atributos y tipos de datos esperados.

#### `test_read_vehicle_not_found`

- **Descripción**: Prueba el escenario donde un vehículo no es encontrado.
- **Endpoints Probados**: `GET /vehicles/{id}`
- **Validación**:
  - Código de estado debe ser 404.
  - La respuesta debe indicar que el vehículo no fue encontrado.

#### `test_read_vehicles`

- **Descripción**: Prueba la obtención de todos los vehículos.
- **Endpoints Probados**: `GET /vehicles/`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista.
  - Cada vehículo en la lista debe tener los atributos y tipos de datos esperados.

#### `test_read_vehicles_with_pagination`

- **Descripción**: Prueba la obtención de vehículos con paginación.
- **Endpoints Probados**: `GET /vehicles/?skip=0&limit=10`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista de longitud 10.
  - Cada vehículo en la lista debe tener los atributos y tipos de datos esperados.


## Documentación de Pruebas integración desarrolladas

---

### `test_maintenance.py`

#### `test_create_and_read_maintenance_order`

- **Descripción**: Prueba la creación y lectura de una orden de mantenimiento.
- **Endpoint Probado**: `POST /maintenance-orders/`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los datos ingresados.
  - Los tipos de datos deben ser los esperados.

#### `test_list_maintenance_orders`

- **Descripción**: Prueba la obtención de todas las órdenes de mantenimiento.
- **Endpoint Probado**: `GET /maintenance-orders/`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista.
  - Cada orden en la lista debe tener los atributos y tipos de datos esperados.

### `test_vehicle.py`

#### `test_create_and_read_vehicle`

- **Descripción**: Prueba la creación y lectura de un vehículo.
- **Endpoint Probado**: `POST /vehicles/`
- **Validación**:
  - Código de estado debe ser 200.
  - Los datos retornados deben coincidir con los datos ingresados.
  - Los tipos de datos deben ser los esperados.

#### `test_list_vehicles`

- **Descripción**: Prueba la obtención de todos los vehículos.
- **Endpoint Probado**: `GET /vehicles/`
- **Validación**:
  - Código de estado debe ser 200.
  - La respuesta debe ser una lista.
  - Cada vehículo en la lista debe tener los atributos y tipos de datos esperados.

---

Con estas pruebas de integración, aseguramos que los endpoints de la API funcionan correctamente y manejan los datos de manera adecuada. Cada prueba valida los datos de entrada y salida según lo especificado en los esquemas de Pydantic y los modelos de SQLAlchemy.

### Ejecución de las Pruebas

Para ejecutar las pruebas:

1. Ejecuta las pruebas con `pytest` en el directorio donde se encuentran los archivos de prueba.

Ejemplo de comando:

```bash
pytest
```