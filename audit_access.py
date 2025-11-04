# audit_access.py
import psycopg2
from psycopg2.extras import RealDictCursor, Json
import os
from datetime import datetime

DB_CFG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbname': os.getenv('DB_NAME', 'privacidad'),
    'user': os.getenv('DB_USER', 'demo'),
    'password': os.getenv('DB_PASS', 'demopass'),
}

def log_access(user, accion, detalle):
    conn = psycopg2.connect(**DB_CFG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO audit_logs (accion, usuario, detalle) VALUES (%s, %s, %s)
    """, (accion, user, Json(detalle)))
    conn.commit()
    cur.close()
    conn.close()

def read_users(requesting_user="analista"):
    conn = psycopg2.connect(**DB_CFG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # ejemplo: devolver solo columnas anonimizadas/pseudonimizadas
    cur.execute("SELECT id, nombre_pseudo, correo_masked, telefono_masked FROM usuarios LIMIT 20")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Registrar la acción
    log_access(requesting_user, "LECTURA_USUARIOS", {"rows_returned": len(rows), "columns": ["id","nombre_pseudo","correo_masked","telefono_masked"], "when": datetime.utcnow().isoformat()})
    return rows

if __name__ == "__main__":
    results = read_users("auditor_john")
    print(results[:5])
