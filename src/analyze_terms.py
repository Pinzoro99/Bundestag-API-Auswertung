"""
analyze_terms.py
-----------------
Analysiert Bundestags-Drucksachen (Rohdaten unter data/raw/drucksache)
auf Basis einer Begriffsliste in config/term_list.json.

Es werden drei Gruppen unterschieden:
- eco_only: Dokumente enthalten nur Begriffe aus Ökologie/Nachhaltigkeit
- sec_only: Dokumente enthalten nur Begriffe aus Sicherheit/Resilienz
- mixed:   Dokumente enthalten aus beiden Bereichen mindestens einen Begriff

Ausgabe: Konsolenübersicht pro Jahr.
"""

import os
import json
from collections import defaultdict
from datetime import datetime

# Pfade
RAW_PATH = "data/raw/drucksache"
TERM_FILE = "config/term_list.json"

# 1) Begriffsliste laden
def load_term_lists():
    """
    Lädt die Begriffslisten aus config/term_list.json und gibt
    zwei Listen (eco_terms, sec_terms) in Kleinschreibung zurück.
    Erwartete Struktur (deine aktuelle):

    {
      "oekologie_nachhaltigkeit": { "keywords": [...] },
      "sicherheit_resilienz": { "keywords": [...] }
    }
    """
    try:
        with open(TERM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        eco_cfg = data.get("oekologie_nachhaltigkeit", {})
        sec_cfg = data.get("sicherheit_resilienz", {})

        eco_terms = [t.lower() for t in eco_cfg.get("keywords", [])]
        sec_terms = [t.lower() for t in sec_cfg.get("keywords", [])]

        # falls du später "aliases" ergänzt
        eco_aliases = [t.lower() for t in eco_cfg.get("aliases", [])]
        sec_aliases = [t.lower() for t in sec_cfg.get("aliases", [])]

        eco_terms = eco_terms + eco_aliases
        sec_terms = sec_terms + sec_aliases

        return eco_terms, sec_terms

    except FileNotFoundError:
        print(f"⚠️  {TERM_FILE} nicht gefunden – verwende Fallback-Begriffe.")
        eco_terms = [
            "nachhaltigkeit",
            "klima",
            "klimaschutz",
            "umweltschutz",
            "ökologie",
            "energiewende",
        ]
        sec_terms = [
            "sicherheit",
            "resilienz",
            "versorgungssicherheit",
            "kritische infrastruktur",
        ]
        return eco_terms, sec_terms


# 2) Schlagworte aus Dokument extrahieren (robust)
def extract_schlagworte(doc):
    """
    Versucht, thematische Metadaten zu holen.
    Viele DIP-Datensätze nutzen:
    - "schlagworte": [ {...}, {...} ]
    - "schlagwort": "..."
    - teils auch "sachgebiet"/"sachgebiete"

    Wir sammeln alles ein und geben eine Liste von Strings (lower) zurück.
    """
    terms = []

    possible_keys = ["schlagworte", "schlagwort", "sachgebiete", "sachgebiet"]

    for key in possible_keys:
        if key not in doc:
            continue

        value = doc[key]

        # Liste von Begriffen / Objekten
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "begriff" in item:
                    terms.append(item["begriff"].lower())
                elif isinstance(item, str):
                    terms.append(item.lower())

        # einzelnes Objekt
        elif isinstance(value, dict) and "begriff" in value:
            terms.append(value["begriff"].lower())

        # einzelner String
        elif isinstance(value, str):
            terms.append(value.lower())

    return terms


# 3) Analyse durchführen
def analyze_documents():
    eco_terms, sec_terms = load_term_lists()

    # year -> counts
    counts = defaultdict(lambda: {
        "total": 0,
        "eco_only": 0,
        "sec_only": 0,
        "mixed": 0,
    })

    # alle JSON-Dateien im Rohdatenordner durchgehen
    for file in os.listdir(RAW_PATH):
        if not file.endswith(".json"):
            continue

        path = os.path.join(RAW_PATH, file)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️  Konnte {path} nicht lesen (kein gültiges JSON).")
                continue

        documents = data.get("documents", [])
        for doc in documents:
            # Jahr bestimmen
            year = "unbekannt"
            date_str = doc.get("datum") or doc.get("aktualisiert")
            if date_str:
                # verschiedene Formate abfangen
                ds = date_str.replace("Z", "+00:00")
                try:
                    year = str(datetime.fromisoformat(ds).year)
                except ValueError:
                    # notfalls Jahr aus den ersten 4 Zeichen
                    year = date_str[:4]

            counts[year]["total"] += 1

            # Schlagworte holen
            doc_terms = extract_schlagworte(doc)
            # zu einem String machen für simples "term in text"
            joined = " ".join(doc_terms)

            has_eco = any(term in joined for term in eco_terms)
            has_sec = any(term in joined for term in sec_terms)

            if has_eco and has_sec:
                counts[year]["mixed"] += 1
            elif has_eco:
                counts[year]["eco_only"] += 1
            elif has_sec:
                counts[year]["sec_only"] += 1
            # wenn weder noch: nur total gezählt

    return counts


if __name__ == "__main__":
    results = analyze_documents()

    # Gesamtsummen
    total_docs = sum(v["total"] for v in results.values())
    total_eco_only = sum(v["eco_only"] for v in results.values())
    total_sec_only = sum(v["sec_only"] for v in results.values())
    total_mixed = sum(v["mixed"] for v in results.values())

    print(f"Gesamtzahl Dokumente: {total_docs}")
    print(f"Nur Ökologie/Nachhaltigkeit: {total_eco_only}")
    print(f"Nur Sicherheit/Resilienz: {total_sec_only}")
    print(f"Beide Themenfelder (mixed): {total_mixed}")
    print()
    print("Pro Jahr:")
    for year in sorted(results.keys()):
        r = results[year]
        print(
            f"{year}: total={r['total']}, "
            f"eco_only={r['eco_only']}, "
            f"sec_only={r['sec_only']}, "
            f"mixed={r['mixed']}"
        )

