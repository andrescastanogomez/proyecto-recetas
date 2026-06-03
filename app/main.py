from dotenv import load_dotenv
load_dotenv()

import os
import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy.exc import OperationalError

from app.models.base import Base, engine
from app.routers import auth, ingredientes, recetas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

print("🔄 Conectando a la base de datos...")

retries = 5

while retries > 0:
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos conectada correctamente")
        break
    except OperationalError:
        retries -= 1
        print(f"⏳ Esperando conexión a la BD... ({retries} intentos restantes)")
        time.sleep(5)
else:
    print("❌ No fue posible conectar la base de datos")

app = FastAPI(
    title="Generador de Recetas Inteligente API",
    description="Backend para inventario y generación de recetas con IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ingredientes.router)
app.include_router(recetas.router)

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"status": "error", "message": f"index.html no encontrado en {INDEX_FILE}"}

@app.get("/web")
def web():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"status": "error", "message": f"index.html no encontrado en {INDEX_FILE}"}

@app.get("/health")
def health():
    return {"status": "online"}