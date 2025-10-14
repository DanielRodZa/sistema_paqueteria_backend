# Sistema de Paquetería - Backend

Este es el backend del sistema de intermediación de entregas, desarrollado con Django y Django REST Framework. Provee una API RESTful para gestionar operaciones, sucursales, vendedores, usuarios y reportes.

## ✨ Características

* **Autenticación y Autorización:** Sistema seguro basado en JWT con tres roles (Administrador, Manager, Recepcionista) y permisos granulares.
* **Gestión de Operaciones:** CRUD completo para paquetes, incluyendo lógica de negocio para:
    * Generación de folios estandarizados (ej. `SUC1-20251006-001`).
    * Cálculo de costos basado en sucursal de origen/destino.
    * Manejo de estado de pago.
    * Fechas de expiración automáticas.
* **Módulos de Gestión:** Endpoints para administrar Sucursales y Vendedores (CRUD completo para Admins).
* **Reportes:** Un endpoint que provee datos agregados para reportes de negocio (conteo, corte de caja) con filtrado por fechas.

## 🛠️ Stack Tecnológico

* **Python 3**
* **Django** & **Django REST Framework**
* **PostgreSQL** (gestionado con Docker)
* **Autenticación:** `djangorestframework-simplejwt`
* **Filtros:** `django-filter`

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para levantar el entorno de desarrollo local.

### 1. Prerrequisitos

* Python 3.10+
* Docker y Docker Compose

### 2. Configuración

1.  **Clona el repositorio** y navega a la carpeta `backend`:
    ```bash
    cd backend
    ```

2.  **Crea el archivo de variables de entorno**. Copia `env.example` (si existe) a `.env` y ajusta los valores si es necesario.
    ```env
    # .env
    DB_NAME=paqueteria_db
    DB_USER=admin
    DB_PASSWORD=admin
    DB_HOST=localhost
    DB_PORT=5432
    ```

3.  **Levanta la base de datos** con Docker:
    ```bash
    docker-compose up -d
    ```

4.  **Crea y activa un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

5.  **Instala las dependencias**. Primero, crea el archivo `requirements.txt`:
    ```bash
    pip freeze > requirements.txt
    ```
    Luego, instálalas (la próxima vez que clones el proyecto):
    ```bash
    pip install -r requirements.txt
    ```

6.  **Aplica las migraciones** para crear las tablas en la base de datos:
    ```bash
    python manage.py migrate
    ```

7.  **Crea un superusuario** para acceder al panel de admin y a la API:
    ```bash
    python manage.py createsuperuser
    ```

8.  **Ejecuta el servidor** de desarrollo:
    ```bash
    python manage.py runserver
    ```
    El servidor estará disponible en `http://127.0.0.1:8000`.

## Endpoints Principales de la API

* `POST /api/token/` - Obtener token de autenticación.
* `GET, POST /api/operaciones/` - Listar (con filtros) o crear operaciones.
* `GET, PATCH, DELETE /api/operaciones/<folio>/` - Ver, actualizar o eliminar una operación.
* `GET, POST /api/sucursales/` - Listar o crear sucursales (solo Admin).
* `GET, POST /api/vendedores/` - Listar o crear vendedores (solo Admin).
* `GET /api/reportes/` - Obtener datos para reportes (solo Admin/Manager).