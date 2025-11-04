CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nombre_original TEXT,
  nombre_pseudo TEXT,
  dni_hash TEXT,
  correo_masked TEXT,
  telefono_masked TEXT,
  direccion_masked TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  accion TEXT,
  usuario TEXT,
  detalle JSONB,
  created_at TIMESTAMP DEFAULT now()
);
