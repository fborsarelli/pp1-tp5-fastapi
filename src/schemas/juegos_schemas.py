from sqlmodel import SQLModel
from .tipos import BoolActivo, Precio, StrCorto, IdCorrecto


# ---------- Género ----------
class GeneroCreate(SQLModel):
    nombre: StrCorto

class GeneroRead(SQLModel):
    id: IdCorrecto
    nombre: StrCorto


# ---------- Juego ----------
class JuegoCreate(SQLModel):
    nombre: StrCorto
    precio: Precio
    genero_id: IdCorrecto
    activo: BoolActivo = True

class JuegoUpdateSchema(SQLModel):
    nombre: StrCorto
    precio: Precio
    genero_id: IdCorrecto
    activo: BoolActivo


# ---------- Anidados ----------
class JuegoRead(SQLModel):
    id: IdCorrecto
    nombre: StrCorto
    precio: Precio
    activo: BoolActivo
    genero: GeneroRead          # objeto anidado

class JuegoSimple(SQLModel):
    id: IdCorrecto
    nombre: StrCorto
    precio: Precio
    activo: BoolActivo

class GeneroReadConJuegos(GeneroRead):
    juegos: list[JuegoSimple] = []   # lista anidada