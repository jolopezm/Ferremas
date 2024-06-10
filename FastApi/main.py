from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from db import engine, session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dollarRate import get_dollar_rate

from transbank.webpay.webpay_plus.transaction import Transaction, IntegrationApiKeys, IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
import models, os, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="toker")

app = FastAPI()
imagenes_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REACT', 'imagenes')
app.mount("/imagenes", StaticFiles(directory=imagenes_directory), name="imagenes")

commerce_code = '597055555532'
api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
options = WebpayOptions(
    commerce_code=commerce_code,
    api_key=api_key,
    integration_type=IntegrationType.TEST
)
transaction = Transaction(options)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/productos")
async def get_productos(db: Session = Depends(get_db)):
    try:
        productos = db.query(models.Producto).all()
        productos_data = [producto.as_dict() for producto in productos]
        return {"productos": productos_data}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {e}")

@app.get("/productos/{item_id}")
async def get_producto_by_id(item_id: int, db: db_dependecy):
    producto = db.query(models.Producto).filter_by(id=item_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"producto": producto.as_dict()}

@app.post("/crea-productos")
async def create_producto(
    nombre: str = Form(...),
    precio: int = Form(...),
    cantidad: int = Form(...),
    descripcion: str = Form(None),
    imagen: UploadFile = File(None),
    imagen_url: str = Form(None),
    categoria_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si la categoría existe
        categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="La categoría especificada no existe")
        
        # Convertir la imagen a bytes si está presente
        imagen_bytes = await imagen.read() if imagen else None
        
        # Crear el producto en la base de datos
        db_producto = models.Producto(
            nombre=nombre, 
            precio=precio, 
            cantidad=cantidad, 
            descripcion=descripcion,
            imagen=imagen_bytes,
            imagen_url=imagen_url,
            categoria_id=categoria_id
        )
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        
        return {"message": f"Producto {nombre} ha sido creado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {e}")

@app.get("/dollar-rate")
def read_dollar_rate():
    rate = get_dollar_rate()
    return {"dollar_rate": rate}
    
@app.put("/actualiza-producto/{producto_id}")
async def update_producto(
    producto_id: int,
    nombre: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    cantidad: Optional[int] = Form(None),
    descripcion: Optional[str] = Form(None),
    imagen: UploadFile = File(None),
    imagen_url: Optional[str] = Form(None),
    categoria_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="La categoría especificada no existe")

        producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if nombre is not None:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if cantidad is not None:
            producto.cantidad = cantidad
        if descripcion is not None:
            producto.descripcion = descripcion
        if imagen is not None:
            producto.imagen = await imagen.read()
        if imagen_url is not None:
            producto.imagen_url = imagen_url
        if categoria_id is not None:
            producto.categoria_id = categoria_id

        db.commit()
        db.refresh(producto)

        return {"message": "Producto actualizado con éxito", "producto": producto.as_dict()}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {e}")

@app.post("/api/init-transaction")
async def init_transaction(data: dict):
    buy_order = data['buy_order']
    session_id = data['session_id']
    amount = data['amount']
    return_url = data['return_url']
    
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.create(buy_order, session_id, amount, return_url)
    
    return {
        "url": resp['url'],
        "token": resp['token']
    }

@app.post("/usuario")
async def registro_usuario(
    usuario: schemas.UsuarioBase, 
    db: Session = Depends(get_db)
):
    try:
        db_user = get_user_by_username(db, nombre=usuario.nombre)
        if db_user:
            raise HTTPException(status_code=400, detail="Nombre de usuario ya existe.")
        
        # Crear el usuario si no existe
        created_user = create_user(db, usuario)
        return {"message": f"Usuario {created_user.nombre} ha sido creado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")

@app.delete("/elimina-producto/{producto_id}")
async def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        db.delete(producto)
        db.commit()
        
        return {"message": "Producto eliminado con éxito"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {e}")

@app.post("/crea-categoria")
async def create_categoria(
    nombre: str = Form(...),
    descripcion: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        categoria = db.query(models.Categoria).filter(models.Categoria.nombre == nombre).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="La categoría especificada ya existe")

        db_categoria = models.Categoria(
            nombre=nombre, 
            descripcion=descripcion,
        )
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        
        return {"message": f"Categoria {nombre} ha sido creada."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear categoria: {e}")
    
@app.get("/categorias/")
async def get_categorias(db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()
    return {"categorias": [categoria.as_dict() for categoria in categorias]}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Nombre o contraseña incorrectos",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token valido"}

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
    user = db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()  # Corrección aquí
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
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