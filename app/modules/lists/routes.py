from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.utils import get_current_user_id
from app.modules.lists import schemas, crud

router = APIRouter(prefix="/lists", tags=["Lists & Items"])

# 1. Crear una lista nueva
@router.post("/", response_model=schemas.ListResponse)
def create_new_list(list_data: schemas.ListCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return crud.create_list(db, list_data, owner_id=current_user_id)

# 2. Agregar ítem a una lista (Solo el dueño puede agregar)
@router.post("/{list_id}/items", response_model=schemas.ItemResponse)
def add_item_to_list(list_id: int, item_data: schemas.ItemCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    # Validar que la lista le pertenezca al usuario
    user_lists = crud.get_user_lists(db, user_id=current_user_id)
    if not any(l.id == list_id for l in user_lists):
        raise HTTPException(status_code=403, detail="No tenés permisos para modificar esta lista.")
    return crud.create_item(db, item_data, list_id)

# 3. Compartir lista con un amigo vía Email
@router.post("/{list_id}/share", status_code=status.HTTP_200_OK)
def share_list(list_id: int, share_data: schemas.ShareListRequest, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user_lists = crud.get_user_lists(db, user_id=current_user_id)
    if not any(l.id == list_id for l in user_lists):
        raise HTTPException(status_code=403, detail="Esta lista no te pertenece.")
    
    result = crud.share_list_by_email(db, list_id, share_data.user_email)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado con ese correo.")
    return {"message": "Lista compartida exitosamente."}

# 4. Ver mis propias listas (OCULTA el estado "is_bought" obligatoriamente)
@router.get("/my-lists", response_model=List[schemas.ListResponse])
def get_my_lists(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    lists = crud.get_user_lists(db, user_id=current_user_id)
    # Regla MVP: El dueño ve todo como NO comprado para mantener la sorpresa
    for l in lists:
        for item in l.items:
            item.is_bought = False
    return lists

# 5. Ver listas que me compartieron (MUESTRA el estado "is_bought" real)
@router.get("/shared-with-me", response_model=List[schemas.ListResponse])
def get_shared_with_me(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return crud.get_shared_lists(db, user_id=current_user_id)

# 6. Marcar ítem como comprado (Solo para usuarios invitados con acceso)
@router.put("/items/{item_id}/buy", response_model=schemas.ItemResponse)
def buy_item(item_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    # Buscar las listas compartidas con el usuario actual para ver si tiene acceso a ese ítem
    shared_lists = crud.get_shared_lists(db, user_id=current_user_id)
    shared_list_ids = [l.id for l in shared_lists]
    
    # Verificar si el ítem pertenece a alguna de esas listas compartidas
    from app.modules.lists.models import ItemModel
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    
    if not item or item.list_id not in shared_list_ids:
        raise HTTPException(status_code=403, detail="No tenés acceso para marcar este ítem.")
        
    return crud.mark_item_as_bought(db, item_id, is_bought=True)