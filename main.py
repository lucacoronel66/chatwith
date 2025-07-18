from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/empresas")
def get_empresas():
    df = pd.read_csv("datos.csv")
    df = df.dropna(subset=["business_name", "number", "category", "country", "city_province", "slug"])

    grouped = df.groupby("category")
    data_by_category = {}

    for category, group in grouped:
        group = group.fillna("")  # evitar NaN en JSON
        data_by_category[category] = group[[
            "business_name", "number", "slug", "country", "city_province"
        ]].to_dict(orient="records")

    return data_by_category