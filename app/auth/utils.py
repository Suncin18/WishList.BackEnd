from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt  # Usamos la librería directa
from app.config import settings

# Encriptar la contraseña
def hash_password(password: str) -> str:
    # 1. Convertir el texto a bytes (UTF-8)
    password_bytes = password.encode('utf-8')
    # 2. Generar la sal (salt) aleatoria
    salt = bcrypt.gensalt()
    # 3. Encriptar y decodificar a string para guardarlo en la base de datos
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

# Verificar si la contraseña en texto plano coincide con la encriptada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convertir ambos a bytes para que bcrypt pueda compararlos
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

# Generar un token JWT firmado (este queda igual)
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependencia para proteger rutas
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de autenticación inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except jwt.PyJWTError:
        raise credentials_exception