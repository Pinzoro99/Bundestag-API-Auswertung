"""
fetch_data.py
-----------------
Dieses Skript ruft Bundestags-Dokumente über die DIP-API ab
und speichert die Ergebnisse als JSON-Dateien unter data/raw/.

Abhängigkeiten:
- config/settings.json (API-Parameter, Zeitraum, Endpunkte)
- .env (API-Key)
- utils.py (Logging, File Handling)
"""

import os
import json
import requests
from datetime import datetime
from utils import setup_logging, save_json

# TODO:
# 1. settings.json laden
# 2. API-Key aus Umgebungsvariable lesen
# 3. Daten für Endpunkte /drucksache und /vorgang abrufen (Paginierung beachten)
# 4. Ergebnisse in data/raw/ speichern

def fetch_data():
    """
    Führt die API-Abfrage für /drucksache und /vorgang aus.
    """
    pass  # To be implemented

if __name__ == "__main__":
    setup_logging()
    fetch_data()
