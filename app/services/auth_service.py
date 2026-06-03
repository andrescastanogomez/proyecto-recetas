# app/services/auth_service.py

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.models.base import get_db, UsuarioModel as Usuario


# ==========================================
# CONFIGURACIÓN JWT
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "supersecretkey123_cambiame_en_produccion"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================================
# BCRYPT
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================
# OAUTH2
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


# ==========================================
# HASH PASSWORD
# ==========================================

def obtener_password_hash(password: str):
    return pwd_context.hash(password)


# ==========================================
# VERIFICAR PASSWORD
# ==========================================

def verificar_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================
# CREAR TOKEN JWT
# ==========================================

def crear_token_acceso(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = (
            datetime.utcnow()
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================================
# OBTENER USUARIO AUTENTICADO
# ==========================================

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.username == username
        )
        .first()
    )

    if usuario is None:
        raise credentials_exception

    return usuario