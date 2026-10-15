from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models.juego import Juego
from src.models.genero import Genero
from src.routers.juegos import juegos_routers
from src.routers.generos import generos_routers

app = FastAPI()
app.title = "TP 5"

app.include_router(juegos_routers, tags=["Juegos"], prefix="/juegos")
app.include_router(generos_routers, tags=["Géneros"], prefix="/generos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)