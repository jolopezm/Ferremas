from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated, Optional
import models, schemas
import os
from db import engine, session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dollarRate import get_dollar_rate
from transbank.webpay.webpay_plus.transaction import Transaction, IntegrationApiKeys, IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank import webpay

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

@app.post("/sign-in")
async def sign_in(
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    direccion: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        db_cliente = models.Cliente(
            nombre=nombre,
            email=email,
            password=password,
            direccion=direccion
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        
        return {"message": f"Cliente {nombre} ha sido creado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cliente: {e}")

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
