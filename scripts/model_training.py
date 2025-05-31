# 📦 Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
import joblib
import os

# 📥 Chargement des données nettoyées
df = pd.read_csv("data/processed/cleaned_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 🧠 Feature engineering
df["dayofweek"] = df["Date"].dt.dayofweek  # Jour de la semaine

# 🎯 Variables explicatives et cible
X = df[["Product line", "City", "Unit price", "dayofweek"]]
y = df["Quantity"]

# 🔤 Encodage des colonnes catégorielles (✅ paramètre corrigé)
encoder = OneHotEncoder(sparse_output=False)
X_encoded = encoder.fit_transform(X[["Product line", "City"]])
X_numeric = X[["Unit price", "dayofweek"]].values

# 🔗 Fusion des colonnes encodées et numériques
X_final = np.concatenate([X_encoded, X_numeric], axis=1)

# 🔀 Séparation en train/test
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# 🌲 Entraînement du modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔎 Évaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Erreur quadratique moyenne (MSE) : {mse:.2f}")

# 💾 Sauvegarde du modèle et de l’encodeur
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/demand_model.pkl")
joblib.dump(encoder, "models/encoder.pkl")

# 📤 Génération du CSV de prédictions
X_raw = X.iloc[X_test.argmax(axis=1)]
X_raw["Predicted Quantity"] = y_pred

# Export
os.makedirs("Output", exist_ok=True)
X_raw.to_csv("../PROJET IA_M1/Output/prediction.csv", index=False)
print("[✅] Fichier prediction.csv exporté.")
