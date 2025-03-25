from fastapi import FastAPI, APIRouter
import pandas as pd

# Cargamos el dataset
movies = pd.read_csv("C:/Users/JuanPablo/Desktop/Kazan/Henry/PI_1/movies.csv")

# Aseguramos que las fechas estén en formato datetime
movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")

app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes = mes.lower()
    if mes not in meses:
        return {"error": "Mes inválido"}

    cantidad = movies[movies["release_date"].dt.month == meses[mes]].shape[0]
    return {f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    dia = dia.lower()
    if dia not in dias:
        return {"error": "Día inválido"}

    cantidad = movies[movies["release_date"].dt.dayofweek == dias[dia]].shape[0]
    return {f"{cantidad} películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    pelicula = movies[movies["title"].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}

    pelicula = pelicula.iloc[0]
    return {
        "titulo": pelicula["title"],
        "año": pelicula["release_date"].year,
        "score": pelicula["popularity"]
    }


