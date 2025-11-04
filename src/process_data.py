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
from datetime import datetime
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
    try:
        with open("config/settings.json", "r", encoding="utf-8") as config_file:
            settings = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    raw_path = settings.get("storage", {}).get("raw_data_path", "data/raw/")
    processed_path = settings.get("storage", {}).get("processed_data_path", "data/processed/")

    drucksache_docs = []
    vorgang_docs = []

    if not os.path.isdir(raw_path):
        raise FileNotFoundError(f"Rohdatenverzeichnis nicht gefunden: {raw_path}")

    for root_dir, _, files in os.walk(raw_path):
        for file_name in sorted(files):
            if not file_name.endswith(".json"):
                continue

            file_path = os.path.join(root_dir, file_name)
            data = load_json(file_path)
            documents = data.get("documents", [])

            if "drucksache" in file_name:
                drucksache_docs.extend(documents)
            elif "vorgang" in file_name:
                vorgang_docs.extend(documents)

    def normalize_list(value):
        if isinstance(value, list):
            normalized = []
            for item in value:
                if isinstance(item, dict):
                    candidate = item.get("name") or item.get("text") or item.get("label")
                    if candidate:
                        normalized.append(str(candidate))
                elif item is not None:
                    normalized.append(str(item))
            return normalized
        if value is None:
            return []
        return [str(value)]

    def extract_vorgangs_id(vorgangsbezug):
        if isinstance(vorgangsbezug, dict):
            return (
                vorgangsbezug.get("id")
                or vorgangsbezug.get("vorgangId")
                or vorgangsbezug.get("vorgangsId")
            )
        if isinstance(vorgangsbezug, list):
            for item in vorgangsbezug:
                if isinstance(item, dict):
                    extracted = (
                        item.get("id")
                        or item.get("vorgangId")
                        or item.get("vorgangsId")
                    )
                    if extracted:
                        return extracted
        return None

    def combine_text_parts(parts):
        cleaned_parts = []
        for part in parts:
            if isinstance(part, list):
                cleaned_parts.extend([p for p in part if p])
            elif part:
                cleaned_parts.append(str(part))
        return " ".join(cleaned_parts).strip()

    def parse_year(date_string):
        if not date_string:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return datetime.strptime(date_string[: len(fmt)], fmt).year
            except ValueError:
                continue
        try:
            return int(date_string[:4])
        except (TypeError, ValueError):
            return None

    processed_drucksache = []
    for doc in drucksache_docs:
        vorgangs_id = extract_vorgangs_id(doc.get("vorgangsbezug"))
        schlagworte = normalize_list(doc.get("schlagworte"))
        sachgebiete = normalize_list(doc.get("sachgebiete"))
        combined_text = combine_text_parts(
            [
                doc.get("titel"),
                doc.get("abstract"),
                schlagworte,
                sachgebiete,
            ]
        )
        processed_drucksache.append(
            {
                "drucksacheId": doc.get("id"),
                "vorgangsId": vorgangs_id,
                "titel": doc.get("titel"),
                "abstract": doc.get("abstract"),
                "schlagwort": schlagworte,
                "sachgebiet": sachgebiete,
                "datum": doc.get("datum"),
                "typ": doc.get("typ"),
                "urheber": doc.get("urheber"),
                "text": combined_text,
                "jahr": parse_year(doc.get("datum")),
                "quelle": "drucksache",
            }
        )

    processed_vorgang = []
    for doc in vorgang_docs:
        schlagworte = normalize_list(doc.get("schlagworte"))
        sachgebiete = normalize_list(doc.get("sachgebiete"))
        combined_text = combine_text_parts(
            [
                doc.get("titel"),
                schlagworte,
                sachgebiete,
            ]
        )
        processed_vorgang.append(
            {
                "vorgangsId": doc.get("id"),
                "titel": doc.get("titel"),
                "initiative": doc.get("initiative"),
                "schlagwort": schlagworte,
                "sachgebiet": sachgebiete,
                "aktualisiert": doc.get("aktualisiert"),
                "vorgangstyp": doc.get("vorgangstyp"),
                "legislaturperiode": doc.get("legislaturperiode"),
                "text": combined_text,
                "jahr": parse_year(doc.get("aktualisiert")),
                "quelle": "vorgang",
            }
        )

    vorgang_map = {entry.get("vorgangsId"): entry for entry in processed_vorgang if entry.get("vorgangsId")}

    combined_records = []

    for drucksache in processed_drucksache:
        matched_vorgang = vorgang_map.get(drucksache.get("vorgangsId"))
        combined_text = combine_text_parts(
            [
                drucksache.get("text"),
                matched_vorgang.get("text") if matched_vorgang else None,
            ]
        )

        jahr = drucksache.get("jahr") or (matched_vorgang.get("jahr") if matched_vorgang else None)

        combined_entry = {
            "drucksacheId": drucksache.get("drucksacheId"),
            "vorgangsId": drucksache.get("vorgangsId"),
            "titel": drucksache.get("titel") or (matched_vorgang.get("titel") if matched_vorgang else None),
            "text": combined_text,
            "datum": drucksache.get("datum"),
            "aktualisiert": matched_vorgang.get("aktualisiert") if matched_vorgang else None,
            "jahr": jahr,
            "quelle": "drucksache",
        }

        combined_records.append(combined_entry)

        if matched_vorgang:
            vorgang_map.pop(drucksache.get("vorgangsId"), None)

    for remaining_vorgang in vorgang_map.values():
        combined_records.append(
            {
                "drucksacheId": None,
                "vorgangsId": remaining_vorgang.get("vorgangsId"),
                "titel": remaining_vorgang.get("titel"),
                "text": remaining_vorgang.get("text"),
                "datum": None,
                "aktualisiert": remaining_vorgang.get("aktualisiert"),
                "jahr": remaining_vorgang.get("jahr"),
                "quelle": "vorgang",
            }
        )

    output_path = os.path.join(processed_path, "combined_texts.json")
    save_json(combined_records, output_path)

if __name__ == "__main__":
    process_data()
