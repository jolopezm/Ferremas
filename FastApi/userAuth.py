from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from typing import Optional

import models, schemas
from db import session

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def create_user(db: Session, user: schemas.UsuarioBase):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.Usuario(nombre=user.nombre, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refrescar la instancia para obtener el ID generado
    return db_user

def get_user_by_username(db: Session, nombre: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()

def authenticate_user(nombre: str, password: str, db: Session):
    user = db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token invalido o expirado")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token invalido o expirado")

def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token valido"}
