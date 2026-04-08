# Moduly
import time
import os
from buildURL import makeURL
from machineLearning import machineLearning
from scraper import getPageNumber, savingToDB
#Dane do adresu
marka = 'ford'
model = 'fiesta'
typNadwozia = ''
cenaWidelki = ['', '']
rokProdukcji = ['','']
# petrol, diesel, petrol-lpg, eletric
paliwo = ''
# automatic, manual
skrzyniaBiegow = 'manual'
przebieg = ['', '']
# Wczytywanie danych



if __name__ == '__main__':
    # Wypelnianie adresu
    if os.path.exists(f"models/model-osobowe_{marka}_{model}.pkl"):
        print("Model dla tych danych istnieje!")
        exit(0)
    url = makeURL(marka, model, typNadwozia, rokProdukcji, cenaWidelki, paliwo, skrzyniaBiegow, przebieg)
    number = int(getPageNumber(url))
    for i in range(1, number + 1):
       print(f"\n--- Pobieram stronę {i} z {number} ---")
       url = makeURL(marka, model, typNadwozia, rokProdukcji, cenaWidelki, paliwo, skrzyniaBiegow, przebieg, page=i)
       savingToDB(url, marka, model)
       time.sleep(2)
    machineLearning(f"{marka}_{model}")
