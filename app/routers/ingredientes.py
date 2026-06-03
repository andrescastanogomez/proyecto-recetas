from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.base import get_db, IngredientModel, UsuarioModel
from app.schemas.esquemas import IngredienteCreate, IngredienteResponse
from app.services.auth_service import obtener_usuario_actual

router = APIRouter(
    prefix="/api/ingredientes",
    tags=["Inventario de Ingredientes"]
)


# ==========================================
# ENDPOINT: OBTENER INGREDIENTES (GET)
# ==========================================
@router.get("/", response_model=List[IngredienteResponse])
def obtener_ingredientes(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(obtener_usuario_actual)
):
    ingredientes = db.query(IngredientModel).filter(
        IngredientModel.usuario_id == current_user.id
    ).all()

    return ingredientes


# ==========================================
# ENDPOINT: AGREGAR INGREDIENTE (POST)
# ==========================================
@router.post("/", response_model=IngredienteResponse, status_code=status.HTTP_201_CREATED)
def agregar_ingrediente(
    ingrediente: IngredienteCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(obtener_usuario_actual)
):
    nuevo_ingrediente = IngredientModel(
        nombre=ingrediente.nombre,
        cantidad=ingrediente.cantidad,
        usuario_id=current_user.id
    )

    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)

    return nuevo_ingrediente


# ==========================================
# ENDPOINT: ACTUALIZAR INGREDIENTE (PUT)
# ==========================================
@router.put("/{ingrediente_id}", response_model=IngredienteResponse)
def actualizar_ingrediente(
    ingrediente_id: int,
    ingrediente_actualizado: IngredienteCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(obtener_usuario_actual)
):
    db_ing = db.query(IngredientModel).filter(
        IngredientModel.id == ingrediente_id,
        IngredientModel.usuario_id == current_user.id
    ).first()

    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")

    db_ing.nombre = ingrediente_actualizado.nombre
    db_ing.cantidad = ingrediente_actualizado.cantidad

    db.commit()
    db.refresh(db_ing)

    return db_ing


# ==========================================
# ENDPOINT: ELIMINAR INGREDIENTE (DELETE)
# ==========================================
@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(obtener_usuario_actual)
):
    db_ing = db.query(IngredientModel).filter(
        IngredientModel.id == ingrediente_id,
        IngredientModel.usuario_id == current_user.id
    ).first()

    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")

    db.delete(db_ing)
    db.commit()

    return