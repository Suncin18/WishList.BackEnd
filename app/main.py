from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.modules.users.routes import router as users_router
from app.modules.lists.routes import router as lists_router
from app.auth.routes import router as auth_router

# Esto le dice a SQLAlchemy que cree las tablas en Supabase si no existen al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wish List API",
    description="MVP de Listas de Deseos con arquitectura limpia en Python",
    version="1.0.0"
)

# --- CONFIGURACIÓN DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Puertos de Vite
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite todos los headers (incluyendo el Authorization)
)

# Aquí iremos registrando las rutas de cada módulo más adelante
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(lists_router)

@app.get("/")
def read_root():
    return {"message": "API estructurada correctamente"}