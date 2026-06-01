# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.modelos import Usuario
from app.schemas.esquemas import UsuarioCreate, Token
from app.services.auth_service import obtener_password_hash, verificar_password, crear_token_acceso

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Validar si el usuario ya existe en la base de datos
    db_user = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    # Crear el nuevo usuario con la contraseña encriptada (Bcrypt)
    nuevo_usuario = Usuario(
        username=usuario.username,
        password_hash=obtener_password_hash(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"message": "Usuario registrado con éxito"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar al usuario por su username
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    
    # Verificar existencia y validar contraseña
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Generar y retornar el token JWT
    token_acceso = crear_token_acceso(data={"sub": usuario.username})
    return {"access_token": token_acceso, "token_type": "bearer"}