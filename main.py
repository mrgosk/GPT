from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import datetime

app = FastAPI()

DB_NAME = "mis_datos.db"

# 🧱 Crear tabla si no existe (Render necesita esto si el .db no existe aún)
def crear_tabla_si_no_existe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            contenido TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

crear_tabla_si_no_existe()  # Ejecutar al iniciar la API

# 📦 Modelo para las peticiones POST
class Nota(BaseModel):
    titulo: str
    contenido: str

# 🔍 GET /notas → Ver todas las notas
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

# ➕ POST /notas → Guardar una nueva nota
@app.post("/notas")
def agregar_nota(nota: Nota):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO notas (titulo, contenido, fecha) VALUES (?, ?, ?)",
                   (nota.titulo, nota.contenido, fecha))
    conn.commit()
    conn.close()
    return {"mensaje": "Nota guardada con éxito"}
