from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()

# CORS para permitir acceso desde cualquier origen (solo para pruebas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos desde /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta raíz para mostrar el index.html directamente
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Endpoint para obtener datos agrupados por categoría
@app.get("/empresas")
def get_empresas():
    df = pd.read_csv("datos.csv")

    grouped = df.groupby("category")
    data_by_category = {}

    for category, group in grouped:
        data_by_category[category] = group[[
            "business_name", "number", "slug", "country", "city_province"
        ]].to_dict(orient="records")

    return data_by_category
