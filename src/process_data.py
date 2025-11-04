"""
process_data.py
-----------------
Dieses Skript verarbeitet die rohen JSON-Dateien aus data/raw/,
führt /drucksache und /vorgang über vorgangsId zusammen und
erstellt strukturierte Dateien in data/processed/.

Abhängigkeiten:
- data/raw/
- specs/03_field_mapping.md
- utils.py
"""

import json
import os
from utils import load_json, save_json

# TODO:
# 1. Rohdaten aus data/raw/ einlesen
# 2. Felder laut field_mapping extrahieren
# 3. Kombiniertes Textfeld bilden (titel + abstract + schlagworte + sachgebiete)
# 4. In data/processed/combined_texts.json speichern

def process_data():
    """
    Führt die Zusammenführung und Textfeld-Erstellung durch.
    """
    pass  # To be implemented

if __name__ == "__main__":
    process_data()
