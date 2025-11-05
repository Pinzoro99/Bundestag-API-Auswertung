"""
analyze_terms.py
-----------------
Analysiert Bundestags-Dokumente (JSON) nach thematischen Schlagworten.
Zählt pro Jahr, wie viele Dokumente folgende Themenfelder enthalten:
- ausschließlich Ökologie/Nachhaltigkeit
- ausschließlich Sicherheit/Resilienz
- beide Themenfelder gleichzeitig (Überschneidung)
"""

import os
import json
from collections import defaultdict
from datetime import datetime

RAW_PATH = "data/raw/drucksache"

# Suchbegriffe (je Themenfeld)
ECO_TERMS = ["nachhaltigkeit", "klima", "ökologie", "umweltschutz", "erneuerbar"]
SEC_TERMS = ["sicherheit", "resilienz", "krise", "notfall", "vorsorge"]

def extract_schlagworte(doc):
    """Extrahiert Schlagworte aus dem Dokument (robust für verschiedene Strukturen)."""
    terms = []

    # Mögliche Schlüssel im Dokument
    keys = ["schlagworte", "schlagwort"]

    for key in keys:
        if key not in doc:
            continue
        value = doc[key]
        if isinstance(value, list):
            for s in value:
                if isinstance(s, dict) and "begriff" in s:
                    terms.append(s["begriff"].lower())
                elif isinstance(s, str):
                    terms.append(s.lower())
        elif isinstance(value, dict) and "begriff" in value:
            terms.append(value["begriff"].lower())
        elif isinstance(value, str):
            terms.append(value.lower())

    return terms

def analyze_documents():
    counts = defaultdict(lambda: {
        "total": 0,
        "eco_only": 0,
        "sec_only": 0,
        "mixed": 0
    })

    for file in os.listdir(RAW_PATH):
        if not file.endswith(".json"):
            continue
        path = os.path.join(RAW_PATH, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for doc in data.get("documents", []):
                # Jahr bestimmen
                year = "unbekannt"
                date_str = doc.get("datum") or doc.get("aktualisiert")
                if date_str:
                    try:
                        year = str(datetime.fromisoformat(date_str.replace("Z", "+00:00")).year)
                    except Exception:
                        pass

                counts[year]["total"] += 1

                # Schlagworte extrahieren
                schlagworte = extract_schlagworte(doc)
                text = " ".join(schlagworte)

                # Thema prüfen
                has_eco = any(term in text for term in ECO_TERMS)
                has_sec = any(term in text for term in SEC_TERMS)

                # Kategorisierung
                if has_eco and has_sec:
                    counts[year]["mixed"] += 1
                elif has_eco:
                    counts[year]["eco_only"] += 1
                elif has_sec:
                    counts[year]["sec_only"] += 1

    return counts

if __name__ == "__main__":
    result = analyze_documents()

    total_docs = sum(y["total"] for y in result.values())
    eco_only_total = sum(y["eco_only"] for y in result.values())
    sec_only_total = sum(y["sec_only"] for y in result.values())
    mixed_total = sum(y["mixed"] for y in result.values())

    print(f"Gesamtzahl Dokumente: {total_docs}")
    print(f"Nur Ökologie/Nachhaltigkeit: {eco_only_total}")
    print(f"Nur Sicherheit/Resilienz: {sec_only_total}")
    print(f"Beide Themenfelder (Überschneidung): {mixed_total}\n")

    print("Pro Jahr:")
    for year, stats in sorted(result.items()):
        print(
            f"{year}: total={stats['total']}, eco_only={stats['eco_only']}, "
            f"sec_only={stats['sec_only']}, mixed={stats['mixed']}"
        )
