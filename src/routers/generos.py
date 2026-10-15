from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.database import get_db
from src.models.genero import Genero
from src.schemas.juegos_schemas import GeneroCreate, GeneroRead, GeneroReadConJuegos
from src.schemas.tipos import IdCorrecto

generos_routers = APIRouter()


@generos_routers.get("/", response_model=list[GeneroRead])
async def get_generos(db: Session = Depends(get_db)):
    return db.exec(select(Genero).order_by(Genero.nombre)).all()


@generos_routers.get("/{id}", response_model=GeneroReadConJuegos)
async def get_genero_by_id(id: IdCorrecto, db: Session = Depends(get_db)):
    genero = db.get(Genero, id)
    if genero is None:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero


@generos_routers.post("/", response_model=GeneroRead)
async def crear_genero(genero_nuevo: GeneroCreate, db: Session = Depends(get_db)):
    existente = db.exec(
        select(Genero).where(Genero.nombre == genero_nuevo.nombre)
    ).first()
    if existente:
        raise HTTPException(status_code=409, detail="El género ya existe")

    genero_db = Genero(**genero_nuevo.model_dump())
    db.add(genero_db)
    db.commit()
    db.refresh(genero_db)
    return genero_db