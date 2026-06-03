from pydantic import BaseModel, Field
from typing import List, Optional

# --- ÍTEMS ---
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    link: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    link: Optional[str]
    price: Optional[float]
    is_bought: bool
    list_id: int

    class Config:
        from_attributes = True

# --- LISTAS ---
class ListCreate(BaseModel):
    title: str = Field(..., min_length=1)

class ListResponse(BaseModel):
    id: int
    title: str
    owner_id: int
    items: List[ItemResponse] = []
    shares: List[dict] = [] # Para identificar si una lista ha sido compartida o no

    class Config:
        from_attributes = True

# --- COMPARTIR ---
class ShareListRequest(BaseModel):
    user_email: str  # Compartimos la lista buscando al amigo por su correo