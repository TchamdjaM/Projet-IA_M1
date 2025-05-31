import pandas as pd
from datetime import timedelta
import os

# Chargement du dataset brut
DATA_PATH = "../PROJET IA_M1/data/raw/SuperMarket Analysis.csv"
df = pd.read_csv(DATA_PATH)

# Nettoyage de base
df['Date'] = pd.to_datetime(df['Date'])  # Conversion en datetime

# Ajout d’une durée de vie par type de produit
shelf_life_map = {
    'Food and beverages': 7,
    'Health and beauty': 30,
    'Electronic accessories': 90,
    'Home and lifestyle': 45,
    'Sports and travel': 60,
    'Fashion accessories': 30
}

df['Shelf_life_days'] = df['Product line'].map(shelf_life_map)

# Calcul de la date de péremption simulée
df['Expiration_date'] = df['Date'] + pd.to_timedelta(df['Shelf_life_days'], unit='d')

# Sauvegarde des données nettoyées
os.makedirs("../PROJET IA_M1/data/processed/", exist_ok=True)
df.to_csv("../PROJET IA_M1/data/processed/cleaned_data.csv", index=False)

print("✅ Données nettoyées et enrichies enregistrées.")
