from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Annotated
import models
from db import engine, session
from sqlalchemy.orm import Session

app = FastAPI()

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

@app.get('/producto/{id}')
def mostrar_producto(id: int):
    return {"data": id}

@app.post('/insertar-producto')
def insertar_producto(producto: ProductoBase):
    return {"message": f"producto {producto.nombre} ha sido insertado."}

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/productos/{producto_id}")
async def read_producto(producto_id: int, db: db_dependecy):
    result = db.query(models.Producto).filter(models.Producto.id == producto_id).first
    if not result:
        raise HTTPException(status_code = 404, detail = 'Producto no encontrado')
    return result

@app.post("/productos/")
async def create_producto(producto: ProductoBase, db: db_dependecy):
    db_producto = models.Producto(nombre=producto.nombre, precio=producto.precio, cantidad=producto.cantidad)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"message": f"Producto {producto.nombre} ha sido creado."}
    