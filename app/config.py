import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

# Instancia única para importar en todo el proyecto
settings = Settings()