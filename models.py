from typing import Optional
from sqlmodel import Field, SQLModel

class Editorial(SQLModel, table=True):
    __tablename__ = "editorial"
    ided: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    pais: str

class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    # Usamos el ISBN como llave primaria String o un ID autoincremental según prefieras
    ISBN: str = Field(primary_key=True)
    titulo: str = Field(index=True)
    autor: str
    precio: float
    ided_editorial: Optional[int] = Field(default=None, foreign_key="editorial.ided")


