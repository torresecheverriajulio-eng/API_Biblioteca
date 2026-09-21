from pydantic import BaseModel

class Editorial(BaseModel):
    idEd: int
    nombre: str
    pais: str

class Libro(BaseModel):
    ISBN: str
    titulo: str
    autor: str
    precio: float  # Representación estándar para valores decimales en JSON
