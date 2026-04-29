import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def seed_data():
    try:
        db_url = os.getenv("DATABASE_URL")
        connection = psycopg2.connect(db_url) if db_url else psycopg2.connect(
            host=os.getenv("DB_HOST","localhost"), user=os.getenv("DB_USER","postgres"),
            password=os.getenv("DB_PASSWORD","root"), dbname=os.getenv("DB_NAME","sistemas_informaticos_cea")
        )
        cursor = connection.cursor()

        # Crear admin por defecto si no existe
        import hashlib
        def hash_pw(pw):
            return hashlib.sha256((pw + "sistemas_informaticos_cea_salt").encode()).hexdigest()

        cursor.execute("SELECT id FROM usuarios WHERE email='admin@sistemas.com'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, email, password, rol, estado) VALUES (%s,%s,%s,%s,%s,%s)",
                ("Admin", "CEA", "admin@sistemas.com", hash_pw("admin123"), "administrador", "activo")
            )

        cursor.execute("DELETE FROM contenidos")
        cursor.execute("DELETE FROM modulos")

        MALLA = [
            # ─── NIVEL BÁSICO – 1er SEMESTRE ───
            ("Básico", "1er SEMESTRE – TÉCNICO BÁSICO", [
                ("TALLER DE SISTEMAS OPERATIVOS I", [
                    "Introducción a los sistemas operativos",
                    "Máquinas virtuales",
                    "Administración de recursos de hardware",
                    "Administración de plataforma Windows",
                ]),
                ("MATEMÁTICA PARA LA INFORMÁTICA", [
                    "Fundamentos y Sistemas de Numeración",
                    "Lógica Matemática y Álgebra Booleana",
                    "Teoría de Conjuntos, Relaciones y Funciones",
                    "Sucesiones y series numéricas",
                ]),
                ("PROGRAMACIÓN I-A", [
                    "Diseño de algoritmos",
                    "Lenguaje de programación e IDEs",
                    "Estructuras básicas de control",
                    "Resolución de Problemas y Pruebas de Escritorio",
                ]),
                ("HARDWARE DE COMPUTADORAS I", [
                    "Evolución y generación de computadoras",
                    "Arquitectura y Partes de una computadora",
                    "Instalación de sistemas operativos y software",
                    "Internet de las cosas (IoT)",
                ]),
                ("EMERGENTE I (INTELIGENCIA ARTIFICIAL BÁSICA)", [
                    "Fundamentos de la Inteligencia Artificial",
                    "Uso incorrecto de la IA en la informática",
                    "Limitaciones tecnológicas de la IA actual",
                    "Uso responsable y ético como futuros profesionales",
                ]),
            ]),
            # ─── NIVEL AUXILIAR – 2do SEMESTRE ───
            ("Auxiliar", "2do SEMESTRE – TÉCNICO AUXILIAR", [
                ("TALLER DE SISTEMAS OPERATIVOS II", [
                    "Administración plataforma Linux",
                    "Contenedores y Virtualización Ligera",
                    "Utilitarios de Sistema",
                    "Seguridad y Gestión de Redes en Linux",
                ]),
                ("OFIMÁTICA Y TECNOLOGÍA MULTIMEDIA I", [
                    "Procesador de texto avanzado",
                    "Hoja de cálculo avanzado",
                    "Presentaciones interactivas",
                    "Herramientas Colaborativas en la Nube",
                ]),
                ("PROGRAMACIÓN I-B", [
                    "Estructuras Iterativas (Bucles)",
                    "Programación modular",
                    "Estructuras de Datos Estáticas",
                    "Introducción a la Programación Orientada a Objetos",
                ]),
                ("HARDWARE DE COMPUTADORAS II", [
                    "Software de mantenimiento e imágenes de sistema",
                    "Mantenimiento preventivo",
                    "Mantenimiento correctivo",
                    "Principios de electrónica aplicados",
                ]),
                ("EMERGENTE II (PROMPTS BÁSICOS)", [
                    "Fundamentos de Prompts",
                    "Prompts para tareas ofimáticas y soporte técnico",
                    "Errores comunes en Modelos de Lenguaje",
                    "Buenas prácticas y refinamiento",
                ]),
            ]),
            # ─── NIVEL MEDIO I – 3er SEMESTRE ───
            ("Medio", "3er SEMESTRE – TÉCNICO MEDIO I", [
                ("INGLÉS TÉCNICO", [
                    "Estructuras Gramaticales y Entorno Personal",
                    "Vocabulario de Informática e Internet",
                    "Inglés para Programación y Sistemas de Medida",
                    "Seguridad Industrial y Manuales Técnicos",
                ]),
                ("DISEÑO Y PROGRAMACIÓN WEB I-A", [
                    "Introducción al diseño web",
                    "HTML (Lenguaje de marcas de hipertexto)",
                    "CSS (Hojas de estilo en cascada)",
                    "Diseño Responsivo y Frameworks Básicos",
                ]),
                ("PROGRAMACIÓN I-C", [
                    "Programación Orientada a Objetos (POO Avanzada)",
                    "Modelado de Software",
                    "Estructuras de Datos Lineales",
                    "Listas Enlazadas y Colecciones",
                ]),
                ("OFIMÁTICA Y TECNOLOGÍA MULTIMEDIA II", [
                    "Edición de audio digital",
                    "Edición de video",
                    "Tratamiento de imágenes",
                    "Producción multimedia integral",
                ]),
                ("EMPRENDIMIENTO PRODUCTIVO E IA APLICADA", [
                    "Emprendimiento Productivo en Tecnología",
                    "Prompt Estructurado para Resolución Lógica",
                    "Uso de IA en Programación y Desarrollo",
                    "Mejora de Resultados mediante Técnicas de Prompting",
                ]),
            ]),
            # ─── NIVEL MEDIO II – 4to SEMESTRE ───
            ("Medio", "4to SEMESTRE – TÉCNICO MEDIO II", [
                ("REDES DE COMPUTADORAS I", [
                    "Fundamentos y Topologías de Red",
                    "Medios de Transmisión, Dispositivos y Modelos",
                    "Direccionamiento IP y Subredes",
                    "Protocolos y Servicios en TCP/IP",
                ]),
                ("DISEÑO Y PROGRAMACIÓN WEB I-B", [
                    "Programación Frontend con JavaScript",
                    "Desarrollo de aplicaciones Backend",
                    "Consumo e Integración de APIs",
                    "Administración y publicación de sitios web",
                ]),
                ("BASE DE DATOS I", [
                    "Introducción a Bases de Datos",
                    "Diseño Conceptual: Modelo Entidad-Relación (E-R)",
                    "Diseño Lógico y Normalización",
                    "Lenguaje SQL y Software para Bases de Datos",
                ]),
                ("PROGRAMACIÓN MÓVIL I", [
                    "Introducción a las Tecnologías Móviles",
                    "Arquitectura y Componentes para el Desarrollo",
                    "Diseño de Interfaz (UI) y Experiencia de Usuario (UX)",
                    "Aplicación práctica y conexión IoT (Microcontroladores)",
                ]),
                ("MODALIDADES DE GRADUACIÓN Y PROYECTO FINAL", [
                    "Reglamentación y Elección de Modalidad",
                    "Planificación del Proyecto Tecnológico asistido por IA",
                    "Desarrollo y Generación Estructural con IA",
                    "Iteración, Refinamiento y Defensa Final",
                ]),
            ]),
        ]

        orden = 1
        for nivel, semestre, modulos in MALLA:
            for mod_nombre, temas in modulos:
                cursor.execute(
                    "INSERT INTO modulos (nombre, nivel, subnivel, orden) VALUES (%s,%s,%s,%s) RETURNING id",
                    (mod_nombre, nivel, semestre, orden)
                )
                m_id = cursor.fetchone()[0]
                orden += 1
                for i, tema_nombre in enumerate(temas):
                    cursor.execute(
                        "INSERT INTO contenidos (modulo_id, tipo, titulo, url, tema_num) VALUES (%s,'teoria',%s,'',%s)",
                        (m_id, tema_nombre, i + 1)
                    )

        connection.commit()
        print("Malla Sistemas Informáticos CEA cargada con éxito.")
        return orden - 1

    except Exception as e:
        print(f"Error seed: {e}")
        return 0
    finally:
        if 'connection' in locals() and connection:
            cursor.close(); connection.close()

if __name__ == "__main__":
    seed_data()
