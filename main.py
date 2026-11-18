import os
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, Body
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select
from models import Usuario, Libro, Editorial

app = FastAPI(title="API Biblioteca - Proyecto Final", version="1.0")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

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

# 1. Login: Acepta credenciales por JSON (Body) O por Query Params
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

    consulta = select(Usuario).where(
        Usuario.username == user_val,
        Usuario.password == pass_val
    )
    usuario = session.exec(consulta).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    return {
        "mensaje": f"Bienvenido {usuario.username}",
        "access_token": TOKEN_SECRETO,
        "token_type": "Bearer"
    }

# 2. Listar Libros (Protegido)
@app.get("/libros", dependencies=[Depends(verificar_token)])
def obtener_libros(session: Session = Depends(get_session)):
    return session.exec(select(Libro)).all()

# 3. Listar Editoriales (Protegido)
@app.get("/editorial", dependencies=[Depends(verificar_token)])
def obtener_editoriales(session: Session = Depends(get_session)):
    return session.exec(select(Editorial)).all()

# 4. Buscar Libros por Año (Protegido)
@app.get("/buscar/year/{year}", dependencies=[Depends(verificar_token)])
def buscar_libros_por_year(year: int, session: Session = Depends(get_session)):
    resultados = session.exec(select(Libro).where(Libro.year == year)).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No hay libros registrados en el año {year}")
    return resultados
