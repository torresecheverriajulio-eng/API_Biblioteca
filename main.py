import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel

from models import Book

app = FastAPI()

@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int):
    obj1 = Book(title="O1 - Cien años de soledad", author="Gabriel García Márquez", year=1967)
    obj2 = Book(title="O2 - Introducción a Python", author="Guido van Rossum",year=1991)
    if book_id==1:
        return obj1
    if book_id==2:
        return obj2

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )