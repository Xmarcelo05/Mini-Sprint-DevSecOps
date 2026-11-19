"""API de práctica local con controles básicos de seguridad."""
import os
import secrets
import sqlite3
from contextlib import closing
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()
app = Flask(__name__)
DB_PATH = Path(__file__).with_name("practica.db")


def init_db():
    """Crea la BD y, si se configura, un usuario de demostración con hash."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, "
            "password_hash TEXT NOT NULL)"
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(users)")}
        if "password_hash" not in columns:
            raise RuntimeError(
                "La BD usa el esquema vulnerable anterior. Respalde los datos y "
                "recree practica.db; no se migran contraseñas automáticamente."
            )
        password = os.environ.get("DEMO_ADMIN_PASSWORD")
        if password and not conn.execute(
            "SELECT 1 FROM users WHERE username = ?", ("admin",)
        ).fetchone():
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", generate_password_hash(password)),
            )
        conn.commit()


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="API de práctica")


@app.get("/api/profile")
def profile():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        return jsonify(error="API key no configurada"), 503
    supplied = request.headers.get("X-API-Key", "")
    if not secrets.compare_digest(supplied.encode(), api_key.encode()):
        return jsonify(error="No autorizado"), 401
    return jsonify(user="admin", message="Acceso de demostración")


@app.post("/api/login")
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Se requiere un objeto JSON"), 400
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify(error="Usuario y contraseña deben ser textos"), 400

    with closing(sqlite3.connect(DB_PATH)) as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row and check_password_hash(row[2], password):
        return jsonify(message="Login correcto", user={"id": row[0], "username": row[1]})
    return jsonify(error="Credenciales inválidas"), 401


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
