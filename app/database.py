from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Crear el motor de conexión para PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Crear la fábrica de sesiones (equivalente al DbContext en .NET)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán todos nuestros modelos de base de datos
Base = declarative_base()

# Dependencia para las rutas (Inyección de dependencias nativa de FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna la sesión a la ruta que la solicitó
    finally:
        db.close()  # Se asegura de cerrar la conexión al terminar el request