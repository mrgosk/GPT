from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite3
import datetime

app = FastAPI()

DB_NAME = "mis_datos.db"

class Nota(BaseModel):
    titulo: str
    contenido: str

@app.get("/notas")
def obtener_notas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, contenido, fecha FROM notas")
    filas = cursor.fetchall()
    conn.close()
    return [
        {"id": f[0], "titulo": f[1], "contenido": f[2], "fecha": f[3]}
        for f in filas
    ]

@app.post("/notas")
def agregar_nota(nota: Nota):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO notas (titulo, contenido, fecha) VALUES (?, ?, ?)",
                   (nota.titulo, nota.contenido, fecha))
    conn.commit()
    conn.close()
    return {"mensaje": "Nota guardada"}
