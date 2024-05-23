from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
#this is a test

app = FastAPI()

class Producto(BaseModel):
    nombre: str
    marca: str
    precio: int
    stock: int
    descripcion: Optional[str]

@app.get('/')
def index():
    return {"message": "hola."}

@app.get('/producto/{id}')
def mostrar_producto(id: int):
    return {"data": id}

@app.post('/insertar-producto')
def insertar_producto(producto: Producto):
    return {"message": f"producto {producto.nombre} ha sido insertado."}