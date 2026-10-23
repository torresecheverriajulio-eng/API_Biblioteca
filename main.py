import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select, Field

# ---- 1. MODELOS DE BASE DE DATOS (UNIFICADOS) ----
class Editorial(SQLModel, table=True):
    __tablename__ = "editorial"
    ided: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    pais: str

class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    ISBN: str = Field(primary_key=True)
    titulo: str = Field(index=True)
    autor: str
    precio: float
    ided_editorial: Optional[int] = Field(default=None, foreign_key="editorial.ided")


# ---- 2. CONFIGURACIÓN DEL MOTOR DE BASE DE DATOS ----
DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI(title="API Biblioteca Universitaria")


# ---- 3. EVENTOS Y DEPENDENCIAS ----
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


# ---- 4. RUTAS CRUD (ENDPOINTS) ----

# --- EDITORIALES ---
@app.post("/editorial/", response_model=Editorial, status_code=201)
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


# --- LIBROS ---
@app.post("/books/", response_model=Libro, status_code=201)
def crear_libro(libro: Libro, session: Session = Depends(get_session)):
    if libro.ided_editorial:
        editorial = session.get(Editorial, libro.ided_editorial)
        if not editorial:
            raise HTTPException(status_code=400, detail="La Editorial asignada no existe")
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


