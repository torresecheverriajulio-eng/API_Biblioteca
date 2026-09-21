from fastapi import FastAPI, HTTPException
from models import Libro, Editorial

app = FastAPI(title="API de Biblioteca Universitaria - Práctica")

# Base de datos simulada: Llaves numéricas para las 3 editoriales
editoriales_db = {
    1: Editorial(idEd=1, nombre="Alfaguara", pais="España"),
    2: Editorial(idEd=2, nombre="Planeta", pais="México"),
    3: Editorial(idEd=3, nombre="Anagrama", pais="España")
}

# Base de datos simulada: Llaves numéricas (1 al 5) para los 5 libros
libros_db = {
    1: Libro(ISBN="978-1", titulo="Cien años de soledad", author="Gabriel García Márquez", precio=25.50),
    2: Libro(ISBN="978-2", titulo="Pedro Páramo", author="Juan Rulfo", precio=18.00),
    3: Libro(ISBN="978-3", titulo="Rayuela", author="Julio Cortázar", precio=22.50),
    4: Libro(ISBN="978-4", titulo="Ficciones", author="Jorge Luis Borges", precio=19.99),
    5: Libro(ISBN="978-5", titulo="El Aleph", author="Jorge Luis Borges", precio=15.00)
}

# --- ENDPOINTS (MÉTODOS GET CORREGIDOS Y UNIFICADOS) ---

@app.get("/books/{book_id}", response_model=Libro)
async def obtener_libro(book_id: int):
    """Busca un libro mediante su ID numérico (1-5)"""
    if book_id not in libros_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros_db[book_id]

# Actualizado a /editorial/{id_ed} en singular
@app.get("/editorial/{id_ed}", response_model=Editorial)
async def obtener_editorial(id_ed: int):
    """Busca una editorial mediante su ID numérico (1-3)"""
    if id_ed not in editoriales_db:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editoriales_db[id_ed]
