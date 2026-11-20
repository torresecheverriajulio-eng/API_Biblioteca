from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str

class Editorial(SQLModel, table=True):
    __tablename__ = "editorial"
    ided: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: Optional[str] = None

class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    ISBN: str = Field(primary_key=True)
    titulo: str
    autor: str
    precio: Optional[Decimal] = None
    existencia: int = Field(default=0)
    ided_editorial: Optional[int] = Field(default=None, foreign_key="editorial.ided")
    year: int

