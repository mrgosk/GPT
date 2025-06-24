from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import datetime
from typing import List

app = FastAPI()

DB_NAME = "mis_datos.db"  # Asegúrate de que esté en el mismo directorio que main.py

class Nota(BaseModel):
    titulo: str
    contenido: str

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "🚀 API de notas funcionando correctamente"}

@app.get("/notas", tags=["Notas"])
def obtener_notas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, contenido, fecha FROM notas")
    filas = cursor.fetchall()
    conn.close()
    return [
        {"id": fila[0], "titulo": fila[1], "contenido": fila[2], "fecha": fila[3]}
        for fila in filas
    ]

@app.post("/notas", tags=["Notas"])
def agregar_nota(nota: Nota):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.date.today().isoformat()
    cursor.execute(
        "INSERT INTO notas (titulo, contenido, fecha) VALUES (?, ?, ?)",
        (nota.titulo, nota.contenido, fecha)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "✅ Nota guardada correctamente"}
