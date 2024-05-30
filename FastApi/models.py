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
