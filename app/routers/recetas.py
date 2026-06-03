from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.base import (
    get_db,
    RecetaModel,
    IngredientModel,
    UsuarioModel,
    CalificacionModel
)

from app.schemas.esquemas import (
    RecetaResponse,
    CalificacionCreate,
    CalificacionResponse
)

from app.services.auth_service import obtener_usuario_actual
from app.services.llm_service import generar_receta_llm

router = APIRouter(
    prefix="/api/recetas",
    tags=["Recetas"]
)


# ==========================================
# GENERAR RECETA CON IA
# ==========================================

@router.post("/generar", response_model=RecetaResponse)
def generar_receta(
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(obtener_usuario_actual)
):

    ingredientes_usuario = (
        db.query(IngredientModel)
        .filter(
            IngredientModel.usuario_id == usuario.id
        )
        .all()
    )

    if not ingredientes_usuario:
        raise HTTPException(
            status_code=400,
            detail="No tienes ingredientes registrados"
        )

    lista_ingredientes = [
        ingrediente.nombre
        for ingrediente in ingredientes_usuario
    ]

    receta_ia = generar_receta_llm(
        lista_ingredientes
    )

    nueva_receta = RecetaModel(
        nombre=receta_ia.get(
            "nombre",
            "Receta Generada"
        ),
        ingredientes_receta=json.dumps(
            receta_ia.get("ingredientes", [])
        ),
        pasos=receta_ia.get(
            "pasos",
            ""
        ),
        tiempo_estimado=receta_ia.get(
            "tiempo_estimado",
            "15 min"
        ),
        dificultad=receta_ia.get(
            "dificultad",
            "Fácil"
        ),
        usuario_id=usuario.id
    )

    db.add(nueva_receta)
    db.commit()
    db.refresh(nueva_receta)

    return nueva_receta


# ==========================================
# HISTORIAL DE RECETAS
# ==========================================

@router.get("/", response_model=List[RecetaResponse])
def obtener_historial(
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(
        obtener_usuario_actual
    )
):

    recetas = (
        db.query(RecetaModel)
        .filter(
            RecetaModel.usuario_id == usuario.id
        )
        .order_by(
            RecetaModel.id.desc()
        )
        .all()
    )

    return recetas


# ==========================================
# ELIMINAR RECETA
# ==========================================

@router.delete("/{receta_id}")
def eliminar_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(
        obtener_usuario_actual
    )
):

    receta = (
        db.query(RecetaModel)
        .filter(
            RecetaModel.id == receta_id,
            RecetaModel.usuario_id == usuario.id
        )
        .first()
    )

    if not receta:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )

    db.delete(receta)
    db.commit()

    return {
        "mensaje": "Receta eliminada"
    }


# ==========================================
# CALIFICAR RECETA
# ==========================================

@router.post(
    "/{receta_id}/calificar",
    response_model=CalificacionResponse
)
def calificar_receta(
    receta_id: int,
    calificacion: CalificacionCreate,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(
        obtener_usuario_actual
    )
):

    receta = (
        db.query(RecetaModel)
        .filter(
            RecetaModel.id == receta_id
        )
        .first()
    )

    if not receta:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )

    nueva_calificacion = CalificacionModel(
        puntos=calificacion.puntos,
        usuario_id=usuario.id,
        receta_id=receta.id
    )

    db.add(nueva_calificacion)
    db.commit()
    db.refresh(nueva_calificacion)

    return nueva_calificacion