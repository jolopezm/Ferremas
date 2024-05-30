from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated, Optional
import models, os, requests
from db import engine, session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dollarRate import get_dollar_rate
from imgConvertCompress import compress_image, convert_image_to_base64

app = FastAPI()
# Directorio completo de las imágenes
imagenes_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'REACT', 'imagenes')

# Montar el directorio de imágenes como una ruta estática
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

class ProductoBase(BaseModel):
    nombre: str
    precio: int
    cantidad: int

@app.get('/')
def index():
    return {"message": "hola."}

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
        if not producto or not producto.imagen:
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
    url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions"
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()