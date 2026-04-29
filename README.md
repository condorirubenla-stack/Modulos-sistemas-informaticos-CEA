# Sistemas Informáticos CEA - LMS Platform

Plataforma educativa (LMS) desarrollada para el Centro de Educación Alternativa (CEA), diseñada para gestionar módulos, estudiantes, profesores y evaluaciones, con un enfoque en escalabilidad, seguridad y fácil despliegue.

## 🚀 Arquitectura y Tecnologías

El proyecto utiliza una arquitectura monolítica modular donde el backend (FastAPI) también sirve los archivos estáticos del frontend, simplificando el despliegue en entornos como Railway.

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Base de Datos:** PostgreSQL (psycopg2)
- **Autenticación:** JWT (JSON Web Tokens), OAuth2PasswordBearer
- **Seguridad:** Hashing con SHA-256 (con salt)
- **Servidor ASGI:** Uvicorn

### Frontend
- **Estructura:** HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Diseño:** Responsive, Mobile-First, UI moderna (Glassmorphism, Dark Mode)
- **Componentes:** Dashboards separados por roles (Admin, Profesor, Estudiante)

---

## ⚙️ Guía de Despliegue (Railway)

La plataforma está optimizada para ser desplegada en **Railway** de forma rápida y automatizada mediante Nixpacks.

### 1. Variables de Entorno (Environment Variables)
En el panel de Railway, debes configurar las siguientes variables en el servicio del backend:
- `DATABASE_URL`: URL de conexión a PostgreSQL (Ej: `postgresql://postgres:pass@host:5432/railway`). Railway puede inyectarla automáticamente si enlazas un servicio de Postgres.
- `PORT`: (Opcional) Railway asigna el puerto dinámicamente, Nixpacks lo lee por defecto.

### 2. Comandos de Arranque (Procfile)
El repositorio contiene un archivo `Procfile` en la raíz que instruye a Railway sobre cómo iniciar el servidor:
```bash
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Migraciones y Base de Datos
El sistema incluye una función de "Auto-Migración". Al iniciar el servidor (startup event de Uvicorn), FastAPI llama a `database.init_db()` que:
1. Crea todas las tablas si no existen.
2. Agrega las columnas necesarias.

Para cargar la Malla Curricular y crear el usuario administrador por defecto (`admin@sistemas.com` / `admin123`), se debe visitar el endpoint:
`https://[TU-DOMINIO].up.railway.app/cargar-datos`

---

## 📈 Guía para Escalar el Proyecto

Si la academia crece y necesitas escalar la plataforma, sigue estas recomendaciones:

### 1. Escalamiento de Base de Datos
- **Connection Pooling:** Actualmente se usa `psycopg2.connect()` directo. Para miles de usuarios concurrentes, implementa **PgBouncer** o usa un pool como `asyncpg` con `SQLAlchemy`.
- **Caché:** Implementa **Redis** para almacenar sesiones JWT cacheadas, configuraciones estáticas y la Malla Curricular, reduciendo lecturas a Postgres.

### 2. Escalamiento de Backend (FastAPI)
- **Workers:** En Railway, puedes cambiar el comando de arranque para usar múltiples workers de Uvicorn/Gunicorn:
  `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- **Asincronismo:** Migrar las consultas de la base de datos de síncronas (`psycopg2`) a asíncronas (`asyncpg`) para desbloquear el event loop de FastAPI.

### 3. Separación de Servicios (Microservicios)
- Si el tráfico aumenta demasiado, separa el Frontend y el Backend en dos servicios distintos en Railway.
- Modifica el archivo `frontend/js/api.js` para que `API_URL` apunte al subdominio exclusivo del backend.
- Habilita CORS estricto en FastAPI en lugar de `allow_origins=["*"]`.

### 4. Almacenamiento de Archivos
- Actualmente los materiales (PDFs, videos) se manejan por URLs externas.
- Para subir archivos propios, integra **Amazon S3** o **Cloudinary** en el backend para almacenar documentos sin saturar el disco del servidor.
