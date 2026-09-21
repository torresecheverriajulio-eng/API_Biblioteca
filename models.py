from pydantic import BaseModel

class Editorial(BaseModel):
    idEd: int
    nombre: str
    pais: str

class Libro(BaseModel):
    ISBN: str
    titulo: str
    author: str
    precio: float

