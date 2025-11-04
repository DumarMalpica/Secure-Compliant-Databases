# anonymize_store.py
import pandas as pd
import hashlib
import uuid
import os
from cryptography.fernet import Fernet
import psycopg2
from psycopg2.extras import Json
from datetime import datetime

# CONFIG DB (puedes usar variables de entorno)
DB_CFG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbname': os.getenv('DB_NAME', 'privacidad'),
    'user': os.getenv('DB_USER', 'demo'),
    'password': os.getenv('DB_PASS', 'demopass'),
}

# Generar o leer clave Fernet para pseudonimización reversible
KEYFILE = "fernet.key"
if not os.path.exists(KEYFILE):
    key = Fernet.generate_key()
    with open(KEYFILE, "wb") as f:
        f.write(key)
else:
    key = open(KEYFILE, "rb").read()
fernet = Fernet(key)

def hash_dni(dni, salt="mi_salto_seguro"):
    h = hashlib.sha256(f"{salt}{dni}".encode()).hexdigest()
    return h

def mask_email(email):
    try:
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            local_masked = local[0] + "*"
        else:
            local_masked = local[0] + "*"*(len(local)-2) + local[-1]
        return f"{local_masked}@{domain}"
    except Exception:
        return "***@***"

def mask_phone(phone):
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) <= 4:
        return "*"*len(digits)
    return "*"*(len(digits)-4) + digits[-4:]

def pseudonimize_name_reversible(name):
    token = fernet.encrypt(name.encode()).decode()
    # store token as pseudo; reversible only with key
    return token

def pseudonimize_name_irreversible(name):
    return "USR-" + uuid.uuid4().hex[:10]

def insert_rows(df):
    conn = psycopg2.connect(**DB_CFG)
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO usuarios (nombre_original, nombre_pseudo, dni_hash, correo_masked, telefono_masked, direccion_masked)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row['nombre_original'],
            row['nombre_pseudo'],
            row['dni_hash'],
            row['correo_masked'],
            row['telefono_masked'],
            row['direccion_masked']
        ))
    # audit log
    cur.execute("""
        INSERT INTO audit_logs (accion, usuario, detalle) VALUES (%s, %s, %s)
    """, (
        "ANONIMIZACION",
        os.getenv('USER', 'estudiante'),
        Json({"rows": len(df), "when": datetime.utcnow().isoformat()})
    ))
    conn.commit()
    cur.close()
    conn.close()

def main():
    df = pd.read_csv('dataset_original.csv')
    df2 = pd.DataFrame()
    df2['nombre_original'] = df['nombre']
    # elegir reversible o irreversible
    df2['nombre_pseudo'] = df['nombre'].apply(pseudonimize_name_irreversible)
    df2['dni_hash'] = df['dni'].apply(lambda x: hash_dni(x))
    df2['correo_masked'] = df['correo'].apply(mask_email)
    df2['telefono_masked'] = df['telefono'].apply(mask_phone)
    df2['direccion_masked'] = df['direccion'].apply(lambda s: s[:10] + "...,")
    df2.to_csv('dataset_anonimizado.csv', index=False)
    print("Archivo anonimiz. creado: dataset_anonimizado.csv")
    insert_rows(df2)
    print("Datos insertados en PostgreSQL y audit log creado.")

if __name__ == "__main__":
    main()
