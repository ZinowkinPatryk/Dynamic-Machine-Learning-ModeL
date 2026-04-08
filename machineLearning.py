import joblib
import sqlite3
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def prepareData(baseName):
    conn = sqlite3.connect("base/baza_aut.db")
    df = pd.read_sql(f"SELECT * FROM {baseName}", conn)
    conn.close()

    df['pojemnosc'] = (df['pojemnosc'].astype(str).str.replace('cm3', '', regex=False)
                       .str.strip().str.replace(' ', ''))
    df['pojemnosc'] = pd.to_numeric(df['pojemnosc'], errors='coerce')
    df['moc'] = (df['moc'].astype(str).str.replace('KM', '', regex=False)
                       .str.strip().str.replace(' ', ''))
    df['moc'] = pd.to_numeric(df['moc'], errors='coerce')
    df['przebieg'] = (df['przebieg'].astype(str).str.replace('km', '', regex=False)
                       .str.strip().str.replace(' ', ''))
    df['przebieg'] = pd.to_numeric(df['przebieg'], errors='coerce')
    df['cena'] = (df['cena'].astype(str).str.replace(' ', ''))
    df['cena'] = pd.to_numeric(df['cena'], errors='coerce')
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    df = df.dropna()
    return df


def prepareTrailsAndGoal(baseName):
    df = prepareData(baseName)
    X = df[['Rokprodukcji', 'typ nadwozia', 'pojemnosc', 'moc', 'skrzynia biegow', 'przebieg', 'rodzaj paliwa']]
    y = df['cena']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # OneHot encoding
    textColumn = ['typ nadwozia', 'skrzynia biegow', 'rodzaj paliwa']
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), textColumn)],
        remainder='passthrough'
    )
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('algo', RandomForestRegressor(n_estimators=100, random_state=42))])
    return [model, X_train, X_test, y_train, y_test]

def machineLearning(baseName):
    tab = prepareTrailsAndGoal(baseName)
    model = tab[0]
    X_train, y_train,  = tab[1], tab[3]
    X_test, y_test = tab[2], tab[4]
    print("TRENOWANIE")
    model.fit(X_train, y_train)
    print("TESTOWANIE")
    przewidywane = model.predict(X_test)
    print(f"Przewidywane: {przewidywane}")
    # >0.6 git
    r2 = r2_score(y_test, przewidywane)
    if r2 > 0.6:
        joblib.dump(model, f'models/model-{baseName}.pkl')
        mea = mean_squared_error(y_test, przewidywane)
        print(f"Mean squared error: {mea**0.5:.0f}")
        print(f"R2 score: {r2:.2f}")
    else:
        print("Slaby model wiecej danych!")









