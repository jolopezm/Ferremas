from pydantic import BaseModel
from datetime import date

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    descripcion: str
    categoria_id: int

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    password: str

class TransactionRequestBase(BaseModel):
    buy_order: str
    session_id: str
    amount: int
    return_url: str

class ConfirmTransactionRequest(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TransaccionBase(BaseModel):
    token: str

class OrdenCompraBase(BaseModel):
    id: str
    fecha_compra: date
    usuario_id: int

    class Config:
        from_attributes = True

class DetalleOrdenCompraBase(BaseModel):
    orden_id: str
    producto_id: int
    cantidad: int

    class Config:
        from_attributes = True
