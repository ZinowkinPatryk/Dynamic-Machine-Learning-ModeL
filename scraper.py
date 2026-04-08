import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sqlite3
# Getting otomoto website
def getPageNumber(url):
    response = None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            lista = soup.find('ul', class_="ooa-1vdlgt7")
            if lista:
                a = [li.text.strip() for li in lista.find_all('li')]
                return a[-2]
            else:
                return 1
    except:
        print(response.status_code)
        return 1


def getHTMLText(url):
    response = None
    data = None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = {}
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', target="_self"):
                newResponse = requests.get(link.get('href'), headers=headers)
                if newResponse.status_code == 200:
                    soup2 = BeautifulSoup(newResponse.content, 'html.parser')
                    helper = []
                    current_id = soup2.find('p', class_='e1j3ff6y1 ooa-1kkaon6').text.strip().split()[1]
                    for paramets in soup2.find_all('div', class_="ooa-1jqwucs e127x9ub1"):
                        helper.append(paramets.get('aria-label'))
                    data[current_id] = [soup2.find_all('p', class_="e1kkw2jt0 ooa-1y1j4sq")[0].text,
                                        f'Cena: {soup2.find_all("span", class_="offer-price__number")[0].text}', helper]
    except Exception as e:
        if response is not None:
            print(f"Błąd HTTP: {response.status_code}. Szczegóły: {e}")
        else:
            print(f"Błąd: {e}")
    finally:
        return data


def savingToDB(url, marka, model):
    data = getHTMLText(url)
    if data:
        parsed_data = []
        for car_id, car_info in data.items():
            try:
                if '·' in car_info[0]:
                    rok_produkcji = car_info[0].split('·')[1].strip()
                else:
                    rok_produkcji = car_info[0]
                cena = car_info[1].replace('Cena:', '').strip()
                parametry = {
                    'typ nadwozia': '',
                    'pojemnosc': '',
                    'moc': '',
                    'skrzynia biegow': '',
                    'rodzaj paliwa': '',
                    'przebieg': ''
                }
                for parametr in car_info[2]:
                    if parametr is None:
                        continue
                    elif parametr.startswith('Typ nadwozia'):
                        parametry['typ nadwozia'] = parametr.replace('Typ nadwozia', '').strip()
                    elif parametr.startswith('Pojemność skokowa'):
                        parametry['pojemnosc'] = parametr.replace('Pojemność skokowa', '').strip()
                    elif parametr.startswith('Moc'):
                        parametry['moc'] = parametr.replace('Moc', '').strip()
                    elif parametr.startswith('Skrzynia biegów'):
                        parametry['skrzynia biegow'] = parametr.replace('Skrzynia biegów', '').strip()
                    elif parametr.startswith('Rodzaj paliwa'):
                        parametry['rodzaj paliwa'] = parametr.replace('Rodzaj paliwa', '').strip()
                    elif parametr.startswith('Przebieg'):
                        parametry['przebieg'] = parametr.replace('Przebieg', '').strip()
                wiersz = (
                    car_id,
                    rok_produkcji,
                    parametry['typ nadwozia'],
                    parametry['pojemnosc'],
                    parametry['moc'],
                    parametry['skrzynia biegow'],
                    parametry['rodzaj paliwa'],
                    parametry['przebieg'],
                    cena
                )
                parsed_data.append(wiersz)
            except Exception as e:
                print(f"Pominięto wadliwe ogłoszenie ID {car_id} z powodu błędu: {e}")
        if parsed_data:
            conn = sqlite3.connect('base/baza_aut.db')
            cursor = conn.cursor()
            tableName = f'{marka}_{model}'.replace('-','_').replace(' ', '_').lower()
            cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS {tableName} (
                            id TEXT PRIMARY KEY,
                            Rokprodukcji TEXT,
                            "typ nadwozia" TEXT,
                            pojemnosc TEXT,
                            moc TEXT,
                            "skrzynia biegow" TEXT,
                            "rodzaj paliwa" TEXT,
                            przebieg TEXT,
                            cena TEXT
                        )            
                        ''')
            cursor.executemany(f'''
                        INSERT OR IGNORE INTO {tableName} 
                        (id, Rokprodukcji, "typ nadwozia", pojemnosc, moc, "skrzynia biegow", "rodzaj paliwa", przebieg, cena)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', parsed_data)
            conn.commit()
            conn.close()
            print("Zapisano zawartosc do nowej tabeli")

