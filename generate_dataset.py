# generate_dataset.py
from faker import Faker
import pandas as pd

fake = Faker('es_CO')  # locale opcional
rows = 200  # tamaño del dataset

data = []
for _ in range(rows):
    data.append({
        'nombre': fake.name(),
        'dni': fake.random_int(min=10000000, max=99999999),
        'correo': fake.email(),
        'telefono': fake.phone_number(),
        'direccion': fake.address().replace("\n", ", ")
    })

df = pd.DataFrame(data)
df.to_csv('dataset_original.csv', index=False)
print("Dataset creado: dataset_original.csv (filas: {})".format(len(df)))
