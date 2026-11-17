import os
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel import Session, create_engine, select
from models import Usuario, Libro, Editorial


app = FastAPI(title="API Biblioteca - Proyecto Final", version="1.0")

# Lee la URL de Supabase desde las variables de entorno de Render
DATABASE_URL = os.getenv("DATABASE_URL")

# Ajuste necesario si la URL de Supabase empieza con postgres:// en lugar de postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# Token de seguridad para validar peticiones
TOKEN_SECRETO = "abc123tokenbiblioteca"

def verificar_token(authorization: str = Header(None)):
    if authorization != f"Bearer {TOKEN_SECRETO}":
        raise HTTPException(
            status_code=401,
            detail="Token inválido o ausente. Usa: Bearer abc123tokenbiblioteca"
        )
    return authorization

@app.get("/")
def inicio():
    return {"mensaje": "API Biblioteca en línea"}

# 1. Login: Valida usuario y contraseña contra la tabla 'usuarios' en Supabase
@app.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    consulta = select(Usuario).where(
        Usuario.username == username,
        Usuario.password == password
    )
    usuario = session.exec(consulta).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    return {
        "mensaje": "Autenticación correcta",
        "access_token": TOKEN_SECRETO,
        "token_type": "Bearer"
    }

# 2. GET /libros (Protegido con token)
@app.get("/libros", dependencies=[Depends(verificar_token)])
def obtener_libros(session: Session = Depends(get_session)):
    libros = session.exec(select(Libro)).all()
    return libros

# 3. GET /editorial (Protegido con token)
@app.get("/editorial", dependencies=[Depends(verificar_token)])
def obtener_editoriales(session: Session = Depends(get_session)):
    editoriales = session.exec(select(Editorial)).all()
    return editoriales

# 4. GET /buscar/year/{year} (Protegido con token)
@app.get("/buscar/year/{year}", dependencies=[Depends(verificar_token)])
def buscar_libros_por_year(year: int, session: Session = Depends(get_session)):
    consulta = select(Libro).where(Libro.year == year)
    resultados = session.exec(consulta).all()
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No hay libros registrados en el año {year}")
    return resultados
