from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.database import get_db
from src.models.juego import Juego
from src.models.genero import Genero
from src.schemas.juegos_schemas import JuegoCreate, JuegoUpdateSchema, JuegoRead
from src.schemas.tipos import IdCorrecto, BoolActivo

juegos_routers = APIRouter()

NOT_FOUND = {
    404: {
        "description": "Response not found si no se encuentra el ID",
        "content": {
            "application/json": {
                "example": {"detail": "Juego no encontrado"}
            }
        },
    },
}


def validar_genero(db: Session, genero_id: int):
    if db.get(Genero, genero_id) is None:
        raise HTTPException(status_code=404, detail="Género no encontrado")


# -------------- GET TODOS --------------
@juegos_routers.get("/", response_model=list[JuegoRead])
async def get_juegos(db: Session = Depends(get_db)):
    return db.exec(select(Juego).where(Juego.activo == True)).all()


# -------------- GET BORRADOS LÓGICOS --------------
@juegos_routers.get("/hidden", response_model=list[JuegoRead])
async def get_juegos_ocultos(db: Session = Depends(get_db)):
    return db.exec(select(Juego).where(Juego.activo == False)).all()


# -------------- GET BY ID --------------
@juegos_routers.get("/{id}", responses=NOT_FOUND, response_model=JuegoRead)
async def get_juego_by_id(id: IdCorrecto, db: Session = Depends(get_db)):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is not None:
        return juego_obtenido
    raise HTTPException(status_code=404, detail="Juego no encontrado")


# -------------- POST --------------
@juegos_routers.post("/", response_model=JuegoRead)
async def crear_juego(juego_nuevo: JuegoCreate, db: Session = Depends(get_db)):
    validar_genero(db, juego_nuevo.genero_id)

    juego_db = Juego(**juego_nuevo.model_dump())
    db.add(juego_db)
    db.commit()
    db.refresh(juego_db)
    return juego_db


# -------------- DELETE --------------
@juegos_routers.delete("/{id}", responses=NOT_FOUND, response_model=list[JuegoRead])
async def borrar_juego(
    id: IdCorrecto,
    borrado_logico: BoolActivo = True,
    db: Session = Depends(get_db),
):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is not None:
        if borrado_logico:
            juego_obtenido.activo = False
            db.commit()
            db.refresh(juego_obtenido)
        else:
            db.delete(juego_obtenido)
            db.commit()
        return db.exec(select(Juego)).all()
    raise HTTPException(status_code=404, detail="Juego no encontrado")


# -------------- PUT --------------
@juegos_routers.put("/{id}", responses=NOT_FOUND, response_model=JuegoRead)
async def editar_juego(
    id: IdCorrecto,
    juego_editar: JuegoUpdateSchema,
    db: Session = Depends(get_db),
):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is None:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    validar_genero(db, juego_editar.genero_id)

    juego_obtenido.sqlmodel_update(juego_editar.model_dump())
    db.add(juego_obtenido)
    db.commit()
    db.refresh(juego_obtenido)
    return juego_obtenido