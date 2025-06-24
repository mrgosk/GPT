from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import datetime

app = FastAPI()
DB_NAME = "mis_datos.db"

class Nota(BaseModel):
    titulo: str
    contenido: str

@app.get("/notas")
def get_notas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, contenido, fecha FROM notas")
    notas = cursor.fetchall()
    conn.close()
    return [{"id": n[0], "titulo": n[1], "contenido": n[2], "fecha": n[3]} for n in notas]

@app.post("/notas")
def post_nota(nota: Nota):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO notas (titulo, contenido, fecha) VALUES (?, ?, ?)", (nota.titulo, nota.contenido, fecha))
    conn.commit()
    conn.close()
    return {"mensaje": "Nota guardada"}
