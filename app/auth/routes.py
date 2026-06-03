from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  # <--- Herramienta nativa
from sqlalchemy.orm import Session
from app.database import get_db
from app.modules.users import crud as user_crud
from app.auth import schemas, utils

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Cambiamos 'login_data: schemas.LoginRequest' por la forma nativa de OAuth2
@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm guarda el correo en 'form_data.username'
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Verificar la contraseña
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Generar el token JWT
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = utils.create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}