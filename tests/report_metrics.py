# tests/report_metrics.py
import pandas as pd

orig = pd.read_csv('dataset_original.csv')
anon = pd.read_csv('dataset_anonimizado.csv')

def unique_counts(df, col):
    return df[col].nunique(), len(df)

print("DNI unique before:", unique_counts(orig, 'dni'))
print("Nombre unique before:", unique_counts(orig, 'nombre'))
print("Emails unique before:", unique_counts(orig, 'correo'))

print("Nombre pseudo unique after:", unique_counts(anon, 'nombre_pseudo'))
print("Correo masked unique after:", unique_counts(anon, 'correo_masked'))

# comprobar combinaciones únicas (nombre + direccion) antes
comb_before = orig.groupby(['nombre','direccion']).size().reset_index(name='count')
unique_comb_before = comb_before.shape[0]
print("Combinaciones nombre+direccion (antes):", unique_comb_before)
# después: nombre_pseudo + direccion_masked
comb_after = anon.groupby(['nombre_pseudo','direccion_masked']).size().reset_index(name='count')
print("Combinaciones pseudonombre+direccion (despues):", comb_after.shape[0])
