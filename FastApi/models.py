from sqlalchemy import Boolean, Column, Integer, String, LargeBinary, Float
from sqlalchemy.orm import declarative_base
import base64

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    cantidad = Column(Integer)
    imagen = Column(LargeBinary, nullable=True)  # Tipo bytea para PostgreSQL
    imagen_url = Column(String)

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "imagen": base64.b64encode(self.imagen).decode('utf-8') if self.imagen else None,
            "imagen_url": self.imagen_url
        }
    
class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String)
    password = Column(String)
    direccion = Column(String)
    is_logged_in = Column(Boolean, default=False)

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
            "direccion": self.direccion,
            "is_logged_in": self.is_logged_in
        }
    