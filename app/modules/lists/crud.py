from sqlalchemy.orm import Session
from app.modules.lists import models, schemas
from app.modules.users.models import User

# Crear una lista nueva
def create_list(db: Session, list_data: schemas.ListCreate, owner_id: int):
    db_list = models.ListModel(title=list_data.title, owner_id=owner_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

# Obtener listas del usuario dueño
def get_user_lists(db: Session, user_id: int):
    return db.query(models.ListModel).filter(models.ListModel.owner_id == user_id).all()

# Agregar un ítem a la lista
def create_item(db: Session, item_data: schemas.ItemCreate, list_id: int):
    db_item = models.ItemModel(
        name=item_data.name,
        link=item_data.link,
        price=item_data.price,
        list_id=list_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Compartir lista con otro usuario vía Email
def share_list_by_email(db: Session, list_id: int, email: str):
    # Buscar al usuario invitado por email
    invited_user = db.query(User).filter(User.email == email).first()
    if not invited_user:
        return None
    
    # Crear el registro de permiso
    db_share = models.ListShareModel(list_id=list_id, shared_with_user_id=invited_user.id)
    db.add(db_share)
    db.commit()
    return db_share

# Marcar ítem como comprado
def mark_item_as_bought(db: Session, item_id: int, is_bought: bool):
    db_item = db.query(models.ItemModel).filter(models.ItemModel.id == item_id).first()
    if db_item:
        db_item.is_bought = is_bought
        db.commit()
        db.refresh(db_item)
    return db_item

# Obtener listas que han sido compartidas CON el usuario
def get_shared_lists(db: Session, user_id: int):
    return db.query(models.ListModel).join(models.ListShareModel).filter(
        models.ListShareModel.shared_with_user_id == user_id
    ).all()