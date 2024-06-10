from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: int
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