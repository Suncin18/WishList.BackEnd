from pydantic import BaseModel, EmailStr, Field

# Esquema para recibir los datos de registro (DTO de Entrada)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr  # Valida automáticamente que sea un correo real
    password: str = Field(..., min_length=6)
    gender: str = Field(..., description="Género del usuario")
    age: int = Field(..., gt=0, lt=120)  # Edad mayor a 0 y menor a 120

# Esquema para retornar datos al cliente (DTO de Salida)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    gender: str
    age: int

    # Le dice a Pydantic que lea los datos aunque vengan de un objeto de SQLAlchemy
    class Config:
        from_attributes = True