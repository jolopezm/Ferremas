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

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/productos")
async def get_productos(db: db_dependecy):
    productos = db.query(models.Producto).all()
    productos_nombres = [producto.nombre for producto in productos]
    return {"productos_nombres": productos_nombres}

@app.post("/crea-productos")
async def create_producto(producto: ProductoBase, db: db_dependecy):
    db_producto = models.Producto(nombre=producto.nombre, precio=producto.precio, cantidad=producto.cantidad)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return {"message": f"Producto {producto.nombre} ha sido creado."}
    