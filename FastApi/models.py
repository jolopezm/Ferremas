from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
from db import engine, Base

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Integer)
    cantidad = Column(Integer)