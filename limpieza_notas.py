import pandas as pd
from unidecode import unidecode

#cargar datos
fdatos = pd.read_csv("notas_estudiantes_sucio.csv")

#observar las primeras filas
#print(fdatos.head())

#creamos una copia del dataset
fdatos_nuevo = fdatos.copy()

#quitar acentos y estandarizar
fdatos_nuevo["Carrera"] = fdatos_nuevo["Carrera"].apply(lambda x:unidecode(x.strip().title()) if isinstance(x,str) else x)

#eliminar filas en blanco
fdatos_nuevo = fdatos_nuevo.dropna(subset=["Nombre","Carrera"])

#eliminar duplicados
fdatos_nuevo = fdatos_nuevo.drop_duplicates()

#rellenar valores faltantes de edad con la media
fdatos_nuevo["Edad"] = fdatos_nuevo["Edad"].fillna(fdatos_nuevo["Edad"].mean())
fdatos_nuevo["Edad"] = fdatos_nuevo["Edad"].astype(int)

#borrar espacios en blanco a la izquierda y derecha
fdatos_nuevo["Nombre"] = fdatos_nuevo["Nombre"].str.strip()
fdatos_nuevo["Carrera"] = fdatos_nuevo["Carrera"].str.strip()

#capitalizar nombres y carera
fdatos_nuevo["Nombre"] = fdatos_nuevo["Nombre"].str.capitalize()
fdatos_nuevo["Carrera"] = fdatos_nuevo["Carrera"].str.capitalize()

#eliminar filas con datos faltantes
fdatos_nuevo = fdatos_nuevo.dropna(subset=["Nota1","Nota2","Nota3"])
#fdatos_nuevo = fdatos_nuevo.fillna(0)

#unificamos la carrera
#fdatos_nuevo["Carrera"] = fdatos_nuevo["Carrera"].str.replace("Fisica", "Física")
#fdatos_nuevo["Carrera"] = fdatos_nuevo["Carrera"].str.replace("Matematicas", "Matemáticas")

#creamos una columna con el promedio de las notas
fdatos_nuevo["Promedio"] = fdatos_nuevo[["Nota1","Nota2","Nota3"]].mean(axis=1).round(2)

#clasificacion de desempeño
def clasificar(promedio):
    if promedio>=4.5:
        return "Excelente"
    elif promedio>=3.5:
        return "Bueno"
    elif promedio>=3.0:
        return "Regular"
    else:
        return "Bajo"
    
fdatos_nuevo["Desempeño"] = fdatos_nuevo["Promedio"].apply(clasificar)

#descargar archivo
fdatos_nuevo.to_csv("notas_limpias.csv",index=False)

print(fdatos_nuevo.head())