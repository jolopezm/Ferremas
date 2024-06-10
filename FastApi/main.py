from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated, Optional

from db import engine
from dollarRate import get_dollar_rate
from initTransaction import init_transaction

import models, os, schemas, userAuth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
imagenes_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REACT', 'imagenes')
app.mount("/imagenes", StaticFiles(directory=imagenes_directory), name="imagenes")

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

db_dependecy = Annotated[Session, Depends(userAuth.get_db)]

@app.get("/productos")
async def get_productos(db: Session = Depends(userAuth.get_db)):
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
    db: Session = Depends(userAuth.get_db)
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
    db: Session = Depends(userAuth.get_db)
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
async def init_transaction_endpoint(data: dict):
    return await init_transaction(data)

@app.post("/usuario")
async def registro_usuario(
    usuario: schemas.UsuarioBase, 
    db: Session = Depends(userAuth.get_db)
):
    try:
        db_user = userAuth.get_user_by_username(db, nombre=usuario.nombre)
        if db_user:
            raise HTTPException(status_code=400, detail="Nombre de usuario ya existe.")
        
        # Crear el usuario si no existe
        created_user = userAuth.create_user(db, usuario)
        return {"message": f"Usuario {created_user.nombre} ha sido creado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")

@app.delete("/elimina-producto/{producto_id}")
async def delete_producto(producto_id: int, db: Session = Depends(userAuth.get_db)):
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
    db: Session = Depends(userAuth.get_db)
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
async def get_categorias(db: Session = Depends(userAuth.get_db)):
    categorias = db.query(models.Categoria).all()
    return {"categorias": [categoria.as_dict() for categoria in categorias]}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(userAuth.get_db)):
    return userAuth.login_for_access_token(form_data, db)

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    return await userAuth.verify_user_token(token)
