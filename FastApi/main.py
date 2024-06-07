from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated, Optional
import models, os
from db import engine, session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dollarRate import get_dollar_rate
from imgConvertCompress import compress_image, convert_image_to_base64
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

class ProductoBase(BaseModel):
    nombre: str
    precio: int
    cantidad: int

class ClienteBase(BaseModel):
    nombre: str
    email: str
    password: str
    direccion: str

class TransactionRequestBase(BaseModel):
    buy_order: str
    session_id: str
    amount: int
    return_url: str

class ConfirmTransactionRequest(BaseModel):
    token: str


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
    precio: float = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db),
    imagen: UploadFile = File(None),
    imagen_url: str = Form(...)
):
    try:
        # Verificar si se proporcionó una imagen
        if imagen:
            # Leer el contenido de la imagen y convertirlo a bytes
            imagen_bytes = await imagen.read()
        else:
            # Si no se proporciona una imagen, establecer los bytes de imagen como None
            imagen_bytes = None
        
        # Crear el producto en la base de datos
        db_producto = models.Producto(
            nombre=nombre, 
            precio=precio, 
            cantidad=cantidad, 
            imagen=imagen_bytes,
            imagen_url=imagen_url
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

@app.get("/productos/{producto_id}/imagen")
async def get_imagen_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
        if not producto or not producto.imagen_url:
            raise HTTPException(status_code=404, detail="Producto no encontrado o sin imagen")
        return {"imagen": f"/imagenes/{producto_id}.jpg"}  # Ruta de la imagen estática
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la imagen del producto: {e}")
    
@app.put("/actualiza-producto/{producto_id}")
async def update_producto(
    producto_id: int,
    nombre: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    cantidad: Optional[int] = Form(None),
    imagen: UploadFile = File(None),
    imagen_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Obtener el producto de la base de datos
        producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # Actualizar los campos solo si se proporcionan nuevos valores
        if nombre is not None:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if cantidad is not None:
            producto.cantidad = cantidad
        if imagen is not None:
            producto.imagen = await imagen.read()
        if imagen_url is not None:
            producto.imagen_url = imagen_url

        # Guardar los cambios en la base de datos
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
    
@app.post("/api/confirm-transaction")
async def confirm_transaction(request: ConfirmTransactionRequest):
    token = request.token
    
    tx = Transaction(webpay.WebpayOptions(webpay.IntegrationCommerceCodes.WEBPAY_PLUS, webpay.IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.commit(token)
    
    if not resp or not resp.vci:
        raise HTTPException(status_code=500, detail="Error al confirmar la transacción")
    
    return resp

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
