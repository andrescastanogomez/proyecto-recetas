from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# ESQUEMAS DE USUARIO (Autenticación)
# ==========================================
class UsuarioBase(BaseModel):
    username: str


class UsuarioCreate(UsuarioBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================================
# ESQUEMAS DE INGREDIENTES (Inventario)
# ==========================================
class IngredienteBase(BaseModel):
    nombre: str

    # 🔥 FIX REAL DEL 422:
    # Antes: Optional[str] -> causaba inconsistencias
    # Ahora: float con validación automática de string -> number
    cantidad: Optional[float] = Field(
        default=None,
        description="Cantidad del ingrediente (número)"
    )


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[float] = None


class IngredienteResponse(IngredienteBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True


# ==========================================
# ESQUEMAS DE CALIFICACIÓN (1 a 5 Estrellas)
# ==========================================
class CalificacionCreate(BaseModel):
    puntos: int = Field(..., ge=1, le=5)


class CalificacionResponse(BaseModel):
    id: int
    puntos: int
    usuario_id: int
    receta_id: int

    class Config:
        from_attributes = True


# ==========================================
# ESQUEMAS DE RECETAS
# ==========================================
class RecetaBase(BaseModel):
    nombre: str
    ingredientes_receta: str
    pasos: str
    tiempo_estimado: Optional[str] = None
    dificultad: Optional[str] = None


class RecetaResponse(RecetaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True