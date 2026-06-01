# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base, engine
from app.routers import auth, ingredientes, recetas

# Crear automáticamente las tablas en MySQL al arrancar la aplicación si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generador de Recetas Inteligente API",
    description="Backend robusto para la gestión de inventario e integración con LLM para el examen final.",
    version="1.0.0"
)

# Configuración de CORS para permitir conexiones desde el Frontend sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se puede restringir al dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de los controladores modulares de la API
app.include_router(auth.router)
app.include_router(ingredientes.router)
app.include_router(recetas.router)

# Servir archivos estáticos (Para las vistas HTML/CSS/JS del Frontend y el favicon obligatorio)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "documentacion": "/docs",
        "mensaje": "Bienvenido al Generador de Recetas Inteligente API. Accede a /docs para ver la documentación interactiva."
    }