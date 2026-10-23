import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from modelos import Libro, Editorial

# 1. Configuración del Motor de Base de Datos
# Render inyectará de forma segura la URL de PostgreSQL mediante esta variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:password@localhost:5432/mi_bd")

# Asegurar compatibilidad con el driver de SQLAlchemy y Asyncpg si aplica
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI(title="API de Biblioteca Universitaria - Práctica")

# 2. Ciclo de Vida: Creación automática de tablas en PostgreSQL al arrancar
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Dependencia para asegurar la apertura y cierre correcto de conexiones por cada Request
def get_session():
    with Session(engine) as session:
        yield session

# 3. ENDPOINTS: Operaciones CRUD solicitadas

# --- SECCIÓN EDITORIALES ---

@app.post("/editorial/", response_model=Editorial, status_code=21)
def crear_editorial(editorial: Editorial, session: Session = Depends(get_session)):
    session.add(editorial)
    session.commit()
    session.refresh(editorial)
    return editorial

@app.get("/editorial/{id_ed}", response_model=Editorial)
def obtener_editorial(id_ed: int, session: Session = Depends(get_session)):
    editorial = session.get(Editorial, id_ed)
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editorial


# --- SECCIÓN LIBROS ---

@app.post("/books/", response_model=Libro, status_code=21)
def crear_libro(libro: Libro, session: Session = Depends(get_session)):
    # Validar si la editorial existe antes de ligar el libro (Integridad Referencial)
    if libro.ided_editorial:
        editorial = session.get(Editorial, libro.ided_editorial)
        if not editorial:
            raise HTTPException(status_code=400, detail="La Editorial asignada no existe.")
            
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@app.get("/books/", response_model=List[Libro])
def obtener_todos_los_libros(session: Session = Depends(get_session)):
    return session.exec(select(Libro)).all()

@app.get("/books/{book_id}", response_model=Libro)
def obtener_libro(book_id: str, session: Session = Depends(get_session)):
    libro = session.get(Libro, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.delete("/books/{book_id}")
def eliminar_libro(book_id: str, session: Session = Depends(get_session)):
    libro = session.get(Libro, book_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
    return {"status": "Registro eliminado exitosamente"}

