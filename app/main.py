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
    description=(
        "API de tickets para laboratorios (PostgreSQL + FastAPI). "
        "Act. 3: modelos y CRUD; Act. 4: JWT en `/auth/token`; "
        "Act. 5: `SecurityScopes`, visibilidad de tickets y transiciones de estado."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(laboratorios.router, prefix="/laboratorios", tags=["laboratorios"])
app.include_router(servicios.router, prefix="/servicios", tags=["servicios"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])


@app.get("/", tags=["sistema"])
def root():
    """Punto de entrada con enlaces útiles para desarrollo y documentación."""
    return {
        "service": app.title,
        "version": app.version,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health",
    }


@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}
