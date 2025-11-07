"""
utils.py
-----------------
Hilfsfunktionen für Logging, Dateioperationen und allgemeine Utilities.
"""

import os
import json
import logging
import sys # Benötigt für den StreamHandler
try:
    import pandas as pd # Benötigt für die save_csv Funktion
except ImportError:
    # Fallback, falls Pandas nicht installiert ist (wird für save_csv benötigt)
    pd = None


def setup_logging(log_file="logs/api_fetch.log", console_output=True, level=logging.INFO):
    """
    Initialisiert ein umfassendes Logging-System mit optionaler Konsolenausgabe.
    """
    
    # Entferne alle bestehenden Handler, um doppeltes Logging zu verhindern
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
            
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Grundkonfiguration
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # File Handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Console Handler (StreamHandler)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
        
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(level)
    
    logging.info("Logging initialisiert. Log-Datei: %s", log_file)


def save_json(data, path):
    """
    Speichert JSON-Daten an einem angegebenen Pfad.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logging.error("Konnte JSON-Datei nicht speichern %s: %s", path, e)

def load_json(path):
    """
    Lädt JSON-Dateien. Gibt None bei Fehler zurück.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        logging.error("Konnte JSON-Datei nicht laden oder parsen %s: %s", path, e)
        return None

def save_csv(df, path):
    """
    Speichert DataFrames als CSV. Benötigt Pandas.
    """
    if pd is None:
        logging.error("Pandas ist nicht importiert. CSV-Speicherung fehlgeschlagen.")
        return
        
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        df.to_csv(path, index=False, encoding='utf-8')
    except Exception as e:
        logging.error("Fehler beim Speichern der CSV-Datei %s: %s", path, e)

# Beispiel, falls Sie ein zentrales Konfigurations-Utility benötigen (optional)
# def load_settings(path="config/settings.json"):
#     return load_json(path)
