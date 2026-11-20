import os
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select
from models import Usuario, Libro, Editorial

app = FastAPI(title="API Librería Chiapas - Proyecto Final", version="1.0")

DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

TOKEN_SECRETO = "abc123tokenbiblioteca"

class LoginRequest(BaseModel):
    username: str
    password: str

def verificar_token(authorization: str = Header(None)):
    if authorization != f"Bearer {TOKEN_SECRETO}":
        raise HTTPException(
            status_code=401,
            detail="Acceso denegado. Token inválido o ausente."
        )
    return authorization

@app.get("/")
def inicio():
    return {"mensaje": "API Biblioteca en línea"}

# ==================== AUTENTICACIÓN ====================
@app.post("/login")
def login(
    datos: Optional[LoginRequest] = Body(default=None),
    username: Optional[str] = None,
    password: Optional[str] = None,
    session: Session = Depends(get_session)
):
    user_val = datos.username if datos else username
    pass_val = datos.password if datos else password

    if not user_val or not pass_val:
        raise HTTPException(status_code=400, detail="Debes enviar username y password")

    consulta = select(Usuario).where(Usuario.username == user_val, Usuario.password == pass_val)
    usuario = session.exec(consulta).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    return {
        "mensaje": f"Bienvenido {usuario.username}",
        "access_token": TOKEN_SECRETO,
        "token_type": "Bearer"
    }

# ==================== CONSULTAS PERSONALIZADAS DE LIBROS ====================
# (Deben ir ANTES de /libros/{isbn} para evitar conflictos de rutas)

@app.get("/libros/sinexistencia", dependencies=[Depends(verificar_token)])
def libros_sin_existencia(session: Session = Depends(get_session)):
    return session.exec(select(Libro).where(Libro.existencia == 0)).all()

@app.get("/libros/editorial/{editorial_id}", dependencies=[Depends(verificar_token)])
def libros_por_editorial(editorial_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Libro).where(Libro.ided_editorial == editorial_id)).all()

@app.get("/libros/anio/{anio}", dependencies=[Depends(verificar_token)])
def libros_por_anio(anio: int, session: Session = Depends(get_session)):
    resultados = session.exec(select(Libro).where(Libro.year == anio)).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No hay libros registrados en el año {anio}")
    return resultados

# ==================== CRUD COMPLETO: LIBROS ====================

@app.post("/libros", status_code=201, dependencies=[Depends(verificar_token)])
def crear_libro(libro: Libro, session: Session = Depends(get_session)):
    if session.get(Libro, libro.ISBN):
        raise HTTPException(status_code=400, detail="Ya existe un libro con ese ISBN")
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@app.get("/libros", dependencies=[Depends(verificar_token)])
def obtener_libros(session: Session = Depends(get_session)):
    return session.exec(select(Libro)).all()

@app.get("/libros/{isbn}", dependencies=[Depends(verificar_token)])
def obtener_libro(isbn: str, session: Session = Depends(get_session)):
    libro = session.get(Libro, isbn)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.put("/libros/{isbn}", dependencies=[Depends(verificar_token)])
def actualizar_libro(isbn: str, datos: Libro, session: Session = Depends(get_session)):
    libro = session.get(Libro, isbn)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro.titulo = datos.titulo
    libro.autor = datos.autor
    libro.precio = datos.precio
    libro.existencia = datos.existencia
    libro.ided_editorial = datos.ided_editorial
    libro.year = datos.year
    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro

@app.delete("/libros/{isbn}", dependencies=[Depends(verificar_token)])
def eliminar_libro(isbn: str, session: Session = Depends(get_session)):
    libro = session.get(Libro, isbn)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(libro)
    session.commit()
    return {"mensaje": f"Libro {isbn} eliminado correctamente"}

# ==================== CRUD COMPLETO: EDITORIALES ====================

@app.post("/editoriales", status_code=201, dependencies=[Depends(verificar_token)])
def crear_editorial(editorial: Editorial, session: Session = Depends(get_session)):
    session.add(editorial)
    session.commit()
    session.refresh(editorial)
    return editorial

@app.get("/editoriales", dependencies=[Depends(verificar_token)])
def obtener_editoriales(session: Session = Depends(get_session)):
    return session.exec(select(Editorial)).all()

@app.get("/editoriales/{ided}", dependencies=[Depends(verificar_token)])
def obtener_editorial(ided: int, session: Session = Depends(get_session)):
    editorial = session.get(Editorial, ided)
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editorial

@app.put("/editoriales/{ided}", dependencies=[Depends(verificar_token)])
def actualizar_editorial(ided: int, datos: Editorial, session: Session = Depends(get_session)):
    editorial = session.get(Editorial, ided)
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    editorial.nombre = datos.nombre
    editorial.pais = datos.pais
    session.add(editorial)
    session.commit()
    session.refresh(editorial)
    return editorial

@app.delete("/editoriales/{ided}", dependencies=[Depends(verificar_token)])
def eliminar_editorial(ided: int, session: Session = Depends(get_session)):
    editorial = session.get(Editorial, ided)
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    session.delete(editorial)
    session.commit()
    return {"mensaje": f"Editorial {ided} eliminada correctamente"}


