from sqlalchemy import Column, Integer, String, LargeBinary, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
import base64

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, unique=True)
    descripcion = Column(String, default='Sin descripción')

    productos = relationship("Producto", back_populates="categoria")

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
    imagen = Column(LargeBinary, nullable=True)
    imagen_url = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    categoria = relationship("Categoria", back_populates="productos")
    detalles = relationship('DetalleOrdenCompra', back_populates='producto')

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

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    ordenes = relationship('OrdenCompra', back_populates='usuario')

    def as_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "hashed_password": self.hashed_password
        }

class Transaccion(Base):
    __tablename__ = 'transaccion'
    token = Column(String, primary_key=True, index=True)

    def as_dict(self):
        return {
            'token': self.token
        }

class OrdenCompra(Base):
    __tablename__ = "orden_compra"

    id = Column(String, primary_key=True, index=True)
    fecha_compra = Column(Date)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship("Usuario", back_populates="ordenes")
    detalles = relationship("DetalleOrdenCompra", back_populates="orden")

class DetalleOrdenCompra(Base):
    __tablename__ = "detalle_orden_compra"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(String, ForeignKey("orden_compra.id"))
    producto_id = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)

    orden = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    