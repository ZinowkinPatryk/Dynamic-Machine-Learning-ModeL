#  AutoHelper - Car Price Predictor & Scraper

AutoHelper is a robust Python backend project designed to scrape car market data, store it, and use Machine Learning to predict car prices or evaluate listings. Currently, the ML model is trained specifically for the **Ford Focus**, but the architecture allows for easy expansion to other models. 

The project exposes a RESTful API using FastAPI, making it ready to be integrated with frontend applications.

##  About the Project & Motivation

This project was built primarily as a gateway into the world of **Artificial Intelligence and Machine Learning**. 
The core assumption of the AutoHelper ML model is to evaluate car prices and deals **strictly based on their technical parameters and listing attributes** (such as year of production, mileage, engine capacity, etc.), stripping away emotional or visual factors to determine a fair market value objectively.

##  Key Features

* **Dynamic Web Scraping:** Uses custom logic (`buildURL.py` and `scraper.py`) to generate search URLs and extract live car listing data from automotive marketplaces.
* **Local Database:** Scraped data is structured and saved in a local SQLite database (`baza_aut.db`) for fast access and model training.
* **Machine Learning Prediction:** Contains a dedicated ML module (`machineLearning.py`) to analyze car parameters and predict their market value based on historical data. 
* **Pre-trained Model:** Includes a ready-to-use, serialized ML model for Ford Focus (`model-focus_ford.pkl`).
* **FastAPI Backend:** A fast and modern REST API server (`fastApiSerw.py`) that serves the scraped data and ML predictions to external clients.

##  Future Roadmap

* ** Android Application:** The next major step is to build a dedicated mobile app using **Android Studio**. This app will consume the FastAPI endpoints, allowing users to check car prices, evaluate deals, and browse market trends directly from their smartphones.

##  Project Structure

* `main.py` - The main entry point of the backend application.
* `fastApiSerw.py` - FastAPI server configuration and API endpoints.
* `scraper.py` - Core logic for extracting car listings from the web.
* `buildURL.py` - Helper script to dynamically construct target URLs for the scraper.
* `machineLearning.py` - Data preprocessing, model training, and prediction logic.
* `model-focus_ford.pkl` - Serialized Machine Learning model trained on Ford Focus data.
* `baza_aut.db` - SQLite database storing the scraped car listings.

##  Tech Stack

* **Language:** Python
* **API Framework:** FastAPI
* **Machine Learning:** Scikit-Learn / Pandas (for `.pkl` model handling)
* **Database:** SQLite
* **Mobile (Planned):** Android Studio (Java/Kotlin)
