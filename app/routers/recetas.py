# app/routers/recetas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from typing import List
from app.models.base import get_db
from app.models.modelos import Receta, Ingrediente, Calificacion, Usuario
from app.schemas.esquemas import RecetaResponse, CalificacionCreate, CalificacionResponse
from app.services.auth_service import obtener_usuario_actual
from app.services.llm_service import generar_receta_llm

router = APIRouter(prefix="/api/recetas", tags=["Generador de Recetas"])

@router.post("/generar", response_model=RecetaResponse)
def generar_receta(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    # 1. Obtener los ingredientes del inventario del usuario
    ingredientes_usuario = db.query(Ingrediente).filter(Ingrediente.usuario_id == usuario.id).all()
    if not ingredientes_usuario:
        raise HTTPException(status_code=400, detail="Tu inventario está vacío. Agrega ingredientes primero.")
    
    lista_nombres = [item.nombre for item in ingredientes_usuario]
    
    # 2. Invocar al servicio interno del LLM pasándole la lista
    receta_ia = generar_receta_llm(lista_nombres)
    
    # 3. Guardar la receta estructurada en la BD vinculada al usuario
    nueva_receta = Receta(
        nombre=receta_ia.get("nombre", "Receta sin Nombre"),
        ingredientes_receta=json.dumps(receta_ia.get("ingredientes", [])),
        pasos=receta_ia.get("pasos", "No especificados"),
        tiempo_estimado=receta_ia.get("tiempo_estimado", "N/A"),
        dificultad=receta_ia.get("dificultad", "N/A"),
        usuario_id=usuario.id
    )
    
    db.add(nueva_receta)
    db.commit()
    db.refresh(nueva_receta)
    return nueva_receta

@router.get("/", response_model=List[RecetaResponse])
def obtener_historial_recetas(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    # Ver historial de recetas generadas previamente
    return db.query(Receta).filter(Receta.usuario_id == usuario.id).all()

@router.delete("/{receta_id}", status_code=status.HTTP_200_OK)
def eliminar_receta(receta_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    receta = db.query(Receta).filter(Receta.id == receta_id, Receta.usuario_id == usuario.id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada en tu historial")
    db.delete(receta)
    db.commit()
    return {"message": "Receta eliminada del historial"}

@router.post("/{receta_id}/calificar", response_model=CalificacionResponse)
def calificar_receta(receta_id: int, cal: CalificacionCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
        
    # Validar si ya existe una calificación previa para actualizarla o registrar una nueva (1 a 5 estrellas)
    db_calificacion = db.query(Calificacion).filter(Calificacion.receta_id == receta_id, Calificacion.usuario_id == usuario.id).first()
    if db_calificacion:
        db_calificacion.puntos = cal.puntos
    else:
        db_calificacion = Calificacion(puntos=cal.puntos, usuario_id=usuario.id, receta_id=receta_id)
        db.add(db_calificacion)
        
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion