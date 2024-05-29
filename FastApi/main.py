from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Annotated
import models, requests
from db import engine, session
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dollarRate import get_dollar_rate

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
    productos_data = [producto.as_dict() for producto in productos]
    return {"productos": productos_data}

@app.get("/productos/{item_id}")
async def get_producto_by_id(item_id: int, db: db_dependecy):
    producto = db.query(models.Producto).filter_by(id=item_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"producto": producto.as_dict()}

@app.post("/crea-productos")
async def create_producto(producto: ProductoBase, db: db_dependecy):
    try:
        db_producto = models.Producto(nombre=producto.nombre, precio=producto.precio, cantidad=producto.cantidad)
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return {"message": f"Producto {producto.nombre} ha sido creado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {e}")

@app.get("/dollar-rate")
def read_dollar_rate():
    rate = get_dollar_rate()
    return {"dollar_rate": rate}
    


