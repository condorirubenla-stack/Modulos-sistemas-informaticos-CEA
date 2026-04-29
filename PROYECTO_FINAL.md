# PROYECTO FINAL - Sistemas Informáticos CEA

Este documento detalla los roles, componentes del equipo y funciones desarrolladas durante la creación y despliegue de la Plataforma Educativa (LMS) para el Centro de Educación Alternativa.

## 👥 Equipo de Desarrollo y Roles

### 1. Desarrollador Backend (API & Lógica de Negocio)
**Funciones principales:**
- Diseño de la arquitectura de la API usando **FastAPI**.
- Creación de rutas protegidas con JWT (`/auth`, `/modulos`, `/evaluaciones`).
- Implementación de la lógica de negocio (Inscripción de estudiantes, asignación de profesores, registro de calificaciones).
- Configuración de la conexión a PostgreSQL y scripts de inicialización (`database.py`, `seed_modulos.py`).
- Implementación del servicio de archivos estáticos (`StaticFiles`) para integrar el frontend dentro del mismo servidor.

### 2. Desarrollador Frontend (UI/UX)
**Funciones principales:**
- Creación de interfaces de usuario modernas, responsivas y atractivas utilizando **HTML5, CSS3 y JavaScript**.
- Diseño de los tres perfiles principales: Administrador (`admin/dashboard.html`), Profesor (`profesor/dashboard.html`) y Estudiante (`student/dashboard.html`).
- Implementación del diseño Glassmorphism y la experiencia Mobile-First.
- Consumo asíncrono de la API mediante la función `fetch()` (`api.js`).
- Renderizado dinámico de la Malla Curricular y reportes de progreso.

### 3. Diseñador de Base de Datos (DBA)
**Funciones principales:**
- Modelado del esquema relacional (Entidad-Relación) para `usuarios`, `modulos`, `contenidos`, `evaluaciones` y `progreso`.
- Generación de las sentencias SQL (`CREATE TABLE`, `ALTER TABLE`) para la inicialización automática.
- Mantenimiento de la integridad referencial (`ON DELETE CASCADE`) y optimización de las consultas (SQL Injections prevention usando tuplas en `psycopg2`).

### 4. Especialista en QA / Tester
**Funciones principales:**
- Pruebas unitarias de los endpoints de la API (Login, Roles, Restricciones).
- Verificación del correcto funcionamiento del CORS y los Tokens JWT.
- Pruebas de estrés y conectividad en el entorno de despliegue real.
- Pruebas de usabilidad (UX) en dispositivos móviles para asegurar la responsividad.
- Identificación de bugs críticos (como el fallo de la ruta relativa en producción) y su posterior reporte al equipo.

### 5. Ingeniero DevOps (Despliegue y CI/CD)
**Funciones principales:**
- Configuración del entorno de producción en **Railway**.
- Creación de archivos de configuración de despliegue: `Procfile` y `requirements.txt`.
- Solución de problemas de enrutamiento web y variables de entorno (`DATABASE_URL`, `$PORT`).
- Monitoreo de logs de construcción (Nixpacks Build Logs) y del servidor en vivo (HTTP Logs).
- Estrategia de unificación de repositorios para evitar colisiones de servicios en la nube.

### 6. Documentador Técnico
**Funciones principales:**
- Redacción del `README.md` detallando la tecnología, dependencias y guías de escalamiento.
- Registro de la Malla Curricular oficial en `seed_modulos.py`.
- Creación de este documento (`PROYECTO_FINAL.md`) para el registro formal del proyecto.
- Comentado de código clave para facilitar el mantenimiento futuro por otros desarrolladores.

---

## 🏆 Resumen del Proyecto

El resultado final es un Sistema de Gestión de Aprendizaje (LMS) robusto, escalable y 100% funcional en la nube, que permite al instituto CEA gestionar toda su Malla Curricular desde el Nivel Básico hasta el Técnico Medio II, ofreciendo una experiencia educativa de primer nivel tanto para estudiantes como para docentes.
