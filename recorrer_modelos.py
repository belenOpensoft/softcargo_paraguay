import os
import django

# Configurar Django para ejecutar el script independientemente del servidor
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cargosystem.settings")
django.setup()

from django.apps import apps

tablas = {}

for model in apps.get_models():
    #print(f"Tabla: {model._meta.db_table} - Modelo: {model.__name__}")
    if model.__name__ not in tablas:
        tablas[model.__name__]=model._meta.db_table
    else:
        print(f'Tabla repetida: {model.__name__}')

        for key,value in tablas.items():
            if key == model.__name__:
                print(model._meta.db_table)

