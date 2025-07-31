# Event Management API

API RESTful para la gestión de eventos, categorías y usuarios. Desarrollada con Django REST Framework, permite la administración completa de eventos con funcionalidades de CRUD, autenticación JWT, documentación Swagger y soft delete.

## 🚀 Características

- **Gestión de Eventos**: CRUD completo para eventos
- **Gestión de Categorías**: Organización de eventos por categorías
- **Gestión de Usuarios**: Administración de usuarios con roles
- **Autenticación JWT**: Seguridad basada en tokens
- **Documentación API**: Documentación interactiva con Swagger
- **Soft Delete**: Eliminación lógica de registros
- **Auditoría**: Registro de fechas y usuarios de creación/modificación
- **Internacionalización**: Soporte para múltiples idiomas

## 🛠️ Tecnologías

- **Python 3.8+**
- **Django 4.2+**
- **Django REST Framework**
- **PostgreSQL** (opcional) SQLite (por defecto)
- **JWT** para autenticación
- **drf-yasg** para documentación Swagger
- **Docker** (opcional)

## 📋 Requisitos Previos
- Python 3.13
- PostgreSQL 13+(recomendado) o SQlite3 (desarrollo)
- Django 5.2.4
- Django REST Framework 3.16 

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/HEAM275/Event_Management_API.git
cd Event_Management_API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Crear la base de datos
-- Opcional, si deseas usar PostgreSQL

-- Crear la base de datos en el gestor 
-- cambiar la configuracion por defecto de la base de datos en el archivo settings.py

-- Ejecutar las migraciones para crear las tablas en la base de datos
python manage.py makemigrations (authentication,manager,events)
python manage.py migrate

### 3. Iniciar el servidor
python manage.py runserver

### 4. Acceder a la documentación Swagger
http://localhost:8000/swagger/

### 5. Para ayuda o soporte contactar
- [email](abreuharold38@gmail.com)



