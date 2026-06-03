import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship
)

# ==========================================
# CONFIGURACIÓN BASE DE DATOS
# ==========================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://db_user:db_password@localhost:3306/recetas_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ==========================================
# DEPENDENCIA DB
# ==========================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# USUARIOS
# ==========================================

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    ingredientes = relationship(
        "IngredientModel",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    recetas = relationship(
        "RecetaModel",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


# ==========================================
# INGREDIENTES
# ==========================================

class IngredientModel(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(
        String(100),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    usuario = relationship(
        "UsuarioModel",
        back_populates="ingredientes"
    )


# ==========================================
# RECETAS
# ==========================================

class RecetaModel(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(
        String(200),
        nullable=False
    )

    ingredientes_receta = Column(
        Text,
        nullable=False
    )

    pasos = Column(
        Text,
        nullable=False
    )

    tiempo_estimado = Column(
        String(50)
    )

    dificultad = Column(
        String(50)
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    usuario = relationship(
        "UsuarioModel",
        back_populates="recetas"
    )

    # AGREGAR ESTO
    calificaciones = relationship(
        "CalificacionModel",
        back_populates="receta",
        cascade="all, delete-orphan"
    )
# ==========================================
# CALIFICACIONES
# ==========================================

class CalificacionModel(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)

    puntos = Column(Integer, nullable=False)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    receta_id = Column(
        Integer,
        ForeignKey("recetas.id"),
        nullable=False
    )

    usuario = relationship(
        "UsuarioModel"
    )

    receta = relationship(
        "RecetaModel",
        back_populates="calificaciones"
    )