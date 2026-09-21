from fastapi import FastAPI, HTTPException
from models import Libro, Editorial

app = FastAPI(title="API de Biblioteca Universitaria")

# Requerimiento 3: Creación de base de datos simulada en memoria
editoriales_db = {
    1: Editorial(idEd=1, nombre="Alfaguara", pais="España"),
    2: Editorial(idEd=2, nombre="Planeta", pais="México"),
    3: Editorial(idEd=3, nombre="Anagrama", pais="España"),
    4: Editorial(idEd=4, nombre="Fondo de Cultura Económica", pais="México")
}

libros_db = {
    "978-1": Libro(ISBN="978-1", titulo="Cien años de soledad", autor="Gabriel García Márquez", precio=25.50),
    "978-2": Libro(ISBN="978-2", titulo="Pedro Páramo", autor="Juan Rulfo", precio=18.00),
    "978-3": Libro(ISBN="978-3", titulo="Rayuela", autor="Julio Cortázar", precio=22.50),
    "978-4": Libro(ISBN="978-4", titulo="Ficciones", autor="Jorge Luis Borges", precio=19.99),
    "978-5": Libro(ISBN="978-5", titulo="El Aleph", autor="Jorge Luis Borges", precio=15.00)
}

# Requerimiento 2: Dos métodos de tipo GET con control de excepciones

@app.get("/libros/{isbn}", response_model=Libro)
async def obtener_libro(isbn: str):
    """Consulta un libro por su código ISBN"""
    if isbn not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado en el sistema")
    return libros_db[isbn]

@app.get("/editoriales/{id_ed}", response_model=Editorial)
async def obtener_editorial(id_ed: int):
    """Consulta una editorial por su Identificador (idEd)"""
    if id_ed not in editoriales_db:
        raise HTTPException(status_code=404, detail="Editorial no encontrada en el sistema")
    return editoriales_db[id_ed]
