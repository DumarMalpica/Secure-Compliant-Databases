# Secure-Compliant-Databases


## 🧩 Estructura principal

Secure-Compliant-Databases/
│
├── anonymize_store.py 
├── audit_access.py 
├── dataset_original.csv 
├── dataset_anonimizado.csv
├── fernet.key 
├── requirements.txt 
└── docker-compose.yml



---

## ⚙️ Requisitos

- Python 3.10+
- Docker y Docker Compose
- Entorno virtual (`venv`)

---

## 🧱 Instalación

1. **Clona el repositorio y entra en el proyecto:**
   ```bash
   git clone https://github.com/tuusuario/Secure-Compliant-Databases.git
   cd Secure-Compliant-Databases

Levanta PostgreSQL con Docker:

bash
Copiar código
docker-compose up -d
Crea y activa el entorno virtual:

bash
Copiar código
python3 -m venv .venv
source .venv/bin/activate
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt

Ejecución
🔸 1. Anonimizar e insertar datos
Ejecuta el script principal:

python anonymize_store.py

🔸 2. Consultar datos anonimizados

python audit_access.py

O directamente desde PostgreSQL:


docker exec -it secure-compliant-databases-postgres-1 psql -U demo -d privacidad

Ejemplo de consulta:

sql

SELECT * FROM usuarios;
SELECT * FROM audit_logs;

