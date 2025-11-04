"""
utils.py
-----------------
Hilfsfunktionen für Logging, Dateioperationen und allgemeine Utilities.
"""

import os
import json
import logging

def setup_logging(log_file="logs/api_fetch.log"):
    """
    Initialisiert ein einfaches Logging-System.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    print("Logging initialisiert:", log_file)

def save_json(data, path):
    """
    Speichert JSON-Daten an einem angegebenen Pfad.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    """
    Lädt JSON-Dateien.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_csv(df, path):
    """
    Speichert DataFrames als CSV.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
