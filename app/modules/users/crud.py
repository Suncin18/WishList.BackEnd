from sqlalchemy.orm import Session
from app.auth.utils import hash_password
from app.modules.users import models, schemas

# Verificar si el correo ya existe
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Crear un usuario nuevo
def create_user(db: Session, user_data: schemas.UserCreate):
    # Encriptar la contraseña real antes de mandarla a Supabase
    hashed_db_password = hash_password(user_data.password)
    
    db_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_db_password,
        gender=user_data.gender,
        age=user_data.age
    )
    
    db.add(db_user)      # Agrega el objeto a la sesión
    db.commit()         # Guarda los cambios en la BD (SaveChanged de .NET)
    db.refresh(db_user)  # Recarga el objeto para obtener el ID generado por la BD
    return db_user