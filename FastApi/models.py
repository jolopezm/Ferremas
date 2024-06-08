from sqlalchemy import Boolean, Column, Integer, String, LargeBinary, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import base64

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, unique=True)
    descripcion = Column(String, default='Sin descripción')

    productos = relationship("Producto", back_populates="categoria")  # Cambiado a "Producto"

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    cantidad = Column(Integer)
    descripcion = Column(String, default='Sin descripción')
    imagen = Column(LargeBinary, nullable=True)  # Tipo bytea para PostgreSQL
    imagen_url = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))  # Cambiado a "categoria.id"

    categoria = relationship("Categoria", back_populates="productos")

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "descripcion": self.descripcion,
            "imagen": base64.b64encode(self.imagen).decode('utf-8') if self.imagen else None,
            "imagen_url": self.imagen_url,
            "categoria_id": self.categoria_id
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
