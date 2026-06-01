# app/models/modelos.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Relaciones: Si se borra un usuario, se borra su inventario e historial en cascada
    ingredientes = relationship("Ingrediente", back_populates="usuario", cascade="all, delete-orphan")
    recetas = relationship("Receta", back_populates="usuario", cascade="all, delete-orphan")
    calificaciones = relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")

class_ingrediente = "Ingrediente"
class Ingrediente(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(String(50), nullable=True)  # Ej: "500g", "2 unidades"
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="ingredientes")

class Receta(Base):
    __tablename__ = "recetas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ingredientes_receta = Column(Text, nullable=False)  # Aquí guardaremos la lista en formato JSON como texto
    pasos = Column(Text, nullable=False)
    tiempo_estimado = Column(String(50))
    dificultad = Column(String(50))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="recetas")
    calificaciones = relationship("Calificacion", back_populates="receta", cascade="all, delete-orphan")

class Calificacion(Base):
    __tablename__ = "calificaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    puntos = Column(Integer, nullable=False)  # Valor del 1 al 5
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="calificaciones")
    receta = relationship("Receta", back_populates="calificaciones")