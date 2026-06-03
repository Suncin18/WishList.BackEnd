from pydantic import BaseModel, EmailStr

# Lo que pide el endpoint para iniciar sesión (Solo email y password como especificaste)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Lo que el backend responde cuando el login es exitoso
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"