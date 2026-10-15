from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .genero import Genero
from src.database import get_db

class Juego(SQLModel, table=True):
    __tablename__ = "juegos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    activo: bool = True

    genero_id: int = Field(foreign_key="generos.id")  # la Foreign Key
    genero: Optional[Genero] = Relationship(back_populates="juegos")

# Los modelos con table=True NO validan datos: la validación
# (largos, rangos) se hace en los schemas.