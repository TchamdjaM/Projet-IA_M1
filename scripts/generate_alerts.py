"""
Ce script analyse les données de vente d’un supermarché, simule les dates de péremption,
et génère des alertes anti-gaspillage (surstock, date courte).
Les résultats sont exportés dans un fichier alerts.csv pour Power BI.
"""

import pandas as pd
from datetime import datetime

# === 1. Chargement des données ===
df = pd.read_csv("data/processed/cleaned_data.csv")  # adapte le chemin si besoin
df["Date"] = pd.to_datetime(df["Date"])

# === 2. Ajout de la date de péremption simulée ===
# Dictionnaire de durée de vie moyenne par catégorie
shelf_life = {
    'Food and beverages': 7,
    'Health and beauty': 30,
    'Electronic accessories': 90,
    'Home and lifestyle': 45,
    'Sports and travel': 60,
    'Fashion accessories': 30
}

df["Shelf_life_days"] = df["Product line"].map(shelf_life)
df["Expiration_date"] = df["Date"] + pd.to_timedelta(df["Shelf_life_days"], unit="d")

# === 3. Génération des alertes ===
# Date actuelle
today = datetime.today()

# Fonction d’alerte
def check_alert(row):
    if row["Expiration_date"] <= today + pd.Timedelta(days=2):
        return "Produit à date courte - PROMO/DON"
    elif row["Quantity"] > df["Quantity"].mean() + df["Quantity"].std():
        return "Surstock - Ajuster commande"
    else:
        return "RAS"

# Appliquer la fonction à chaque ligne
df["Alerte"] = df.apply(check_alert, axis=1)

# === 4. Export du fichier ===
# Colonnes pertinentes pour Power BI
output = df[[
    "Date", "Product line", "Quantity",
    "Expiration_date", "Alerte", "Sales", "City"
]]

# Enregistrement
output_path = "outputs/alerts.csv"
output.to_csv(output_path, index=False)

print(f"[✅] Fichier d’alertes généré : {output_path}")
