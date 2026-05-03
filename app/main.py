from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import auth, laboratorios, servicios, tickets, usuarios


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Mesa de servicios — Laboratorio 3",
    description="API de tickets para laboratorios. Actividad 4: JWT en /auth/token y rutas protegidas.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(laboratorios.router, prefix="/laboratorios", tags=["laboratorios"])
app.include_router(servicios.router, prefix="/servicios", tags=["servicios"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])


@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}
