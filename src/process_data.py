"""
process_data.py
-----------------
Dieses Skript verarbeitet die rohen JSON-Dateien aus data/raw/drucksache,
extrahiert die minimal notwendigen Felder (ID, Titel, Datum, Typ, Urheber) 
und speichert die bereinigten Daten als CSV für die nachfolgende Analyse.

Das Skript ignoriert Vorgangs-Daten und kombiniert KEINE Textfelder, 
um die Analyse auf den Dokumententitel zu fokussieren.
"""

import json
import os
import csv
from datetime import datetime
# Annahme: Sie haben eine einfache load_json Funktion in utils.py
from utils import load_json 

# --- KONFIGURATION ---
# Wir verwenden keine save_json mehr, sondern csv.
RAW_PATH = "data/raw/drucksache"
PROCESSED_FILE = "data/processed/processed_documents.csv"
# ---------------------

def parse_year(date_string):
    """Extrahiert das Jahr aus verschiedenen Datumsformaten."""
    if not date_string:
        return None
    # Wir brauchen nur die ersten 4 Zeichen, da wir nur das Jahr benötigen (z.B. 2023-...)
    try:
        return int(date_string[:4])
    except (TypeError, ValueError):
        return None

def process_data():
    """
    Extrahiert die relevanten Felder aus den /drucksache Rohdaten.
    """
    processed_records = []
    docs_processed = 0

    if not os.path.isdir(RAW_PATH):
        print(f"[FEHLER] Rohdatenverzeichnis nicht gefunden: {RAW_PATH}")
        return

    print(f"[INFO] Starte Verarbeitung von Rohdaten in {RAW_PATH}...")

    # Durchgehen aller JSON-Dateien unter data/raw/drucksache
    for root_dir, _, files in os.walk(RAW_PATH):
        for file_name in sorted(files):
            if not file_name.endswith(".json"):
                continue

            file_path = os.path.join(root_dir, file_name)
            data = load_json(file_path)
            documents = data.get("documents", [])
            
            # Extraktion der minimalen Felder (wie in 03_field_mapping.md definiert)
            for doc in documents:
                processed_records.append(
                    {
                        "drucksacheId": doc.get("id"),
                        "datum": doc.get("datum"),
                        "jahr": parse_year(doc.get("datum")),
                        "titel_raw": doc.get("titel", ""), # Der Titel ist das wichtigste Feld
                        "typ": doc.get("typ"),
                        "urheber": ", ".join(doc.get("urheber", [])) if isinstance(doc.get("urheber"), list) else doc.get("urheber", ""),
                    }
                )
                docs_processed += 1
    
    print(f"[INFO] {docs_processed} Drucksachen-Datensätze verarbeitet.")
    
    # Speichern als CSV
    save_to_csv(processed_records)


def save_to_csv(records):
    """Speichert die Liste der Dictionaries als CSV-Datei."""
    
    if not records:
        print("[WARNUNG] Keine Datensätze zum Speichern vorhanden.")
        return

    # Die Feldnamen basieren auf dem minimalistischen Mapping
    fieldnames = ["drucksacheId", "datum", "jahr", "titel_raw", "typ", "urheber"]
    
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    
    try:
        with open(PROCESSED_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            
        print(f"[INFO] Bereinigte Daten gespeichert unter: {PROCESSED_FILE}")
    except IOError as e:
        print(f"[FEHLER] Konnte bereinigte Daten nicht speichern: {e}")
        
        
if __name__ == "__main__":
    process_data()
