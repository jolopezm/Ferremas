from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Integer)
    cantidad = Column(Integer)
    imagen = Column(LargeBinary, nullable=True)

    def as_dict(self):
        """
        Returns a dictionary representation of the Producto object.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "imagen": self.imagen
        }
