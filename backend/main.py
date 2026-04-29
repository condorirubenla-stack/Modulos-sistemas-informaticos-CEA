import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import auth, modulos, evaluaciones
from database import init_db

load_dotenv()

app = FastAPI(title="Sistemas Informaticos CEA API", description="LMS Backend - Sistemas Informaticos CEA v1.0")

@app.on_event("startup")
def startup_event():
    print("Servidor Sistemas Informaticos CEA iniciado.")
    try:
        init_db()
        print("Base de datos inicializada.")
    except Exception as e:
        print(f"Error init_db en startup: {e}")
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS carnet VARCHAR(50)")
        cur.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS nivel_asignado VARCHAR(100)")
        cur.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'activo'")
        cur.execute("ALTER TABLE modulos ADD COLUMN IF NOT EXISTS subnivel VARCHAR(100)")
        cur.execute("ALTER TABLE modulos ADD COLUMN IF NOT EXISTS orden INT DEFAULT 0")
        cur.execute("ALTER TABLE contenidos ADD COLUMN IF NOT EXISTS tema_num INT DEFAULT 1")
        conn.commit()
        cur.close(); conn.close()
        print("Migracion de columnas completada.")
    except Exception as e:
        print(f"Migracion startup warning: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,         prefix="/auth",         tags=["Authentication"])
app.include_router(modulos.router,      prefix="/modulos",      tags=["Modulos"])
app.include_router(evaluaciones.router, prefix="/evaluaciones", tags=["Evaluaciones"])

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def read_root():
        return RedirectResponse(url="/static/login.html")
else:
    @app.get("/")
    def read_root():
        import os
        return {
            "status": "backend_only", 
            "message": "Frontend not found", 
            "cwd": os.getcwd(), 
            "file": __file__, 
            "frontend_path": frontend_path,
            "root_contents": os.listdir(os.path.dirname(os.path.dirname(__file__))) if os.path.exists(os.path.dirname(os.path.dirname(__file__))) else []
        }

@app.get("/cargar-datos")
def instalar_datos_iniciales():
    """Inicializa tablas, crea usuarios por defecto y carga la malla curricular."""
    try:
        import importlib
        import seed_modulos
        import database
        importlib.reload(database)
        importlib.reload(seed_modulos)
        database.init_db()
        reparados = seed_modulos.seed_data()
        from database import get_db_connection
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute("SELECT email, rol FROM usuarios ORDER BY id")
        users = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM modulos")
        total_mods = cur.fetchone()[0]
        cur.close(); conn.close()
        return {
            "status":           "success",
            "version":          "1.0.0 PRO",
            "modulos_creados":  reparados,
            "total_en_bd":      total_mods,
            "usuarios":         [{"email": u[0], "rol": u[1]} for u in users]
        }
    except Exception as e:
        return {"status": "error", "detalle": str(e)}
