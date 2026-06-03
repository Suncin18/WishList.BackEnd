from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class ListModel(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relaciones para poder hacer consultas tipo 'lista.items' fácilmente
    items = relationship("ItemModel", back_populates="list", cascade="all, delete-orphan")
    shares = relationship("ListShareModel", back_populates="list", cascade="all, delete-orphan")


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)  # Equivalente a decimal en .NET
    is_bought = Column(Boolean, default=False, nullable=False)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)

    list = relationship("ListModel", back_populates="items")


class ListShareModel(Base):
    __tablename__ = "list_shares"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    shared_with_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    list = relationship("ListModel", back_populates="shares")