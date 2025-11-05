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
import logging
import time
import requests
from datetime import datetime
from utils import setup_logging, save_json
from dotenv import load_dotenv

# .env einlesen, damit DIP_API_KEY verfügbar ist
load_dotenv()

def fetch_data():
    """
    Führt die API-Abfrage für /drucksache und /vorgang aus.
    """
    try:
        with open("config/settings.json", "r", encoding="utf-8") as config_file:
            settings = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logging.error("Konfigurationsdatei konnte nicht geladen werden: %s", exc)
        return

    auth_settings = settings.get("auth", {})
    env_var_name = auth_settings.get("env_var_name", "DIP_API_KEY")
    api_key = os.environ.get(env_var_name)
    if not api_key:
        logging.error("API-Key in Umgebungsvariable %s nicht gefunden", env_var_name)
        return

    base_url = settings.get("api_base_url", "https://search.dip.bundestag.de/api/v1")
    endpoints = settings.get("endpoints", {})
    request_params = settings.get("request_params", {}).copy()
    date_range = settings.get("date_range", {})
    raw_storage = settings.get("storage", {}).get("raw_data_path", "data/raw/")

    headers = {"Authorization": f"ApiKey {api_key}"}
    session = requests.Session()

    for endpoint_name, endpoint_path in endpoints.items():
        params = request_params.copy()
        params.setdefault("cursor", "*")

        # für drucksache: nach datum filtern
        if endpoint_name == "drucksache":
            if date_range.get("from"):
                params["f.datum.start"] = date_range["from"]
            if date_range.get("to"):
                params["f.datum.end"] = date_range["to"]
        else:
            # ursprünglicher Stand: für vorgang nach aktualisiert filtern
            if date_range.get("from"):
                params["f.aktualisiert.start"] = date_range["from"]
            if date_range.get("to"):
                params["f.aktualisiert.end"] = date_range["to"]

        page = 1
        while True:
            try:
                response = session.get(
                    f"{base_url}{endpoint_path}",
                    headers=headers,
                    params=params,
                    timeout=30,
                )
            except requests.RequestException as exc:
                logging.error("API-Anfrage fehlgeschlagen (%s): %s", endpoint_name, exc)
                break

            if response.status_code == 429:
                logging.warning("Rate Limit erreicht – erneuter Versuch in 60 Sekunden")
                time.sleep(60)
                continue

            if response.status_code != 200:
                logging.error(
                    "Unerwarteter Statuscode für %s: %s", endpoint_name, response.status_code
                )
                break

            try:
                data = response.json()
            except json.JSONDecodeError as exc:
                logging.error("Fehler beim Dekodieren der Antwort (%s): %s", endpoint_name, exc)
                break

            documents = data.get("documents", [])
            if not documents:
                logging.info("Keine weiteren Dokumente für %s gefunden", endpoint_name)
                break

            timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            file_name = f"{endpoint_name}_{timestamp}_{page:04d}.json"
            save_path = os.path.join(raw_storage, endpoint_name, file_name)
            save_json(data, save_path)
            logging.info("%s: Seite %d gespeichert (%s)", endpoint_name, page, save_path)

            next_cursor = data.get("cursor") or data.get("nextCursor")
            if not next_cursor or next_cursor == params.get("cursor"):
                break

            params["cursor"] = next_cursor
            page += 1

            time.sleep(1)

if __name__ == "__main__":
    setup_logging()
    fetch_data()
