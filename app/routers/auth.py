from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.base import get_db, UsuarioModel as Usuario
from app.schemas.esquemas import UsuarioCreate, Token
from app.services.auth_service import (
    obtener_password_hash,
    verificar_password,
    crear_token_acceso
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    # Verificar si el usuario ya existe
    db_user = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado"
        )

    # Crear usuario con contraseña encriptada
    nuevo_usuario = Usuario(
        username=usuario.username,
        password=obtener_password_hash(usuario.password)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "message": "Usuario registrado con éxito"
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.username == form_data.username
        )
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    if not verificar_password(
        form_data.password,
        usuario.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    token_acceso = crear_token_acceso(
        {"sub": usuario.username}
    )

    return {
        "access_token": token_acceso,
        "token_type": "bearer"
    }