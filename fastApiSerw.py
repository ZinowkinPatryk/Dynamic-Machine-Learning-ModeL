from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import time
from buildURL import makeURL
from machineLearning import machineLearning
from scraper import getPageNumber, savingToDB
app = FastAPI(title="AutoWycena")


class CarRequest(BaseModel):
    model: str
    marka: str
    Rokprodukcji: str
    typ_nadwozia: str
    pojemnosc: int
    moc: int
    skrzynia_biegow: str
    przebieg: int
    rodzaj_paliwa: str


def makePrediction(daneModel):
    model = joblib.load(f'models/model-{daneModel.get("marka")}_{daneModel.get("model")}.pkl')
    dane_dla_algorytmu = {
        "Rokprodukcji": daneModel["Rokprodukcji"],
        "typ nadwozia": daneModel["typ_nadwozia"],
        "pojemnosc": daneModel["pojemnosc"],
        "moc": daneModel["moc"],
        "skrzynia biegow": daneModel["skrzynia_biegow"],
        "przebieg": daneModel["przebieg"],
        "rodzaj paliwa": daneModel["rodzaj_paliwa"]
    }
    df = pd.DataFrame([dane_dla_algorytmu])
    prediction = model.predict(df)[0]
    return {"cena": round(prediction, 2)}


@app.post("/car")
def predict(car: CarRequest):
    daneModel = {
        "model": car.model,
        "marka": car.marka,
        "Rokprodukcji": car.Rokprodukcji,
        "typ_nadwozia": car.typ_nadwozia,
        "pojemnosc": car.pojemnosc,
        "moc": car.moc,
        "skrzynia_biegow": car.skrzynia_biegow,
        "przebieg": car.przebieg,
        "rodzaj_paliwa": car.rodzaj_paliwa,
    }
    if os.path.exists(f"models/model-{daneModel.get('marka')}_{daneModel.get('model')}.pkl"):
        return makePrediction(daneModel)
    else:
        url = makeURL(daneModel.get("marka"), daneModel.get("model"))
        number = int(getPageNumber(url))
        for i in range(1, number + 1):
            print(f"\n--- Pobieram stronę {i} z {number} ---")
            url = makeURL(daneModel.get("marka"), daneModel.get("model"), page=i)
            savingToDB(url,daneModel.get("marka"), daneModel.get("model"))
            time.sleep(2)
        machineLearning(f"{daneModel.get('marka')}_{daneModel.get('model')}")
        return makePrediction(daneModel)
