# app/schemas/esquemas.py
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
    cantidad: Optional[str] = None  # Ejemplo: "500g" o "3 unidades"

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteResponse(IngredienteBase):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

# ==========================================
# ESQUEMAS DE CALIFICACIÓN (1 a 5 Estrellas)
# ==========================================
class CalificacionCreate(BaseModel):
    puntos: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")

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
class RecetaResponse(BaseModel):
    id: int
    nombre: str
    ingredientes_receta: str  # Se almacena como texto plano formateado en JSON
    pasos: str
    tiempo_estimado: Optional[str]
    dificultad: Optional[str]
    usuario_id: int
    
    class Config:
        from_attributes = True