from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from src.database import get_db

if TYPE_CHECKING:
    from .juego import Juego


class Genero(SQLModel, table=True):
    __tablename__ = "generos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)

    juegos: list["Juego"] = Relationship(back_populates="genero")