# app/routers/ingredientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.base import get_db
from app.models.modelos import Ingrediente, Usuario
from app.schemas.esquemas import IngredienteCreate, IngredienteResponse
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(prefix="/api/ingredientes", tags=["Inventario de Ingredientes"])

@router.post("/", response_model=IngredienteResponse)
def crear_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    nuevo_ingrediente = Ingrediente(
        nombre=ingrediente.nombre,
        cantidad=ingrediente.cantidad,
        usuario_id=usuario.id
    )
    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)
    return nuevo_ingrediente

@router.get("/", response_model=List[IngredienteResponse])
def listar_ingredientes(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    # Retorna únicamente los ingredientes asociados al usuario autenticado
    return db.query(Ingrediente).filter(Ingrediente.usuario_id == usuario.id).all()

@router.delete("/{ingrediente_id}", status_code=status.HTTP_200_OK)
def eliminar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    item = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id, Ingrediente.usuario_id == usuario.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado en tu inventario")
    db.delete(item)
    db.commit()
    return {"message": "Ingrediente eliminado correctamente"}