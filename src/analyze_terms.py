"""
analyze_terms.py
----------------
Analysiert die Titel der abgerufenen Drucksachen (data/raw/drucksache)
und prüft, ob sie Begriffe aus
- Ökologie/Nachhaltigkeit
- Sicherheit/Resilienz
enthalten.

Die Begriffe werden aus config/term_list.json geladen.
"""

import os
import json
from collections import defaultdict

DATA_PATH = "data/raw/drucksache"
TERM_FILE = "data/term_list.json"


def load_terms():
    """Liest die Begriffe aus config/term_list.json im Format mit 'categories'."""
    try:
        with open(TERM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[WARNUNG] config/term_list.json nicht gefunden – Fallback wird genutzt.")
        return (
            ["klimaschutz", "nachhaltigkeit", "umweltschutz"],
            ["sicherheit", "resilienz"],
        )

    # wir erwarten: data["categories"]["oekologie_nachhaltigkeit"]["keywords"]
    cats = data.get("categories", {})
    eco_block = cats.get("oekologie_nachhaltigkeit")
    sec_block = cats.get("sicherheit_resilienz")

    if eco_block is None or sec_block is None:
        print("[WARNUNG] 'categories' gefunden, aber erwartete Schlüssel fehlen.")
        print(f"Vorhandene Kategorien: {list(cats.keys())}")
        return (
            ["klimaschutz", "nachhaltigkeit", "umweltschutz"],
            ["sicherheit", "resilienz"],
        )

    eco_terms = [t.lower() for t in eco_block.get("keywords", []) + eco_block.get("aliases", [])]
    sec_terms = [t.lower() for t in sec_block.get("keywords", []) + sec_block.get("aliases", [])]

    print(f"[INFO] {len(eco_terms)} Ökologie/Nachhaltigkeit-Begriffe geladen.")
    print(f"[INFO] {len(sec_terms)} Sicherheit/Resilienz-Begriffe geladen.")
    return eco_terms, sec_terms


def analyze_documents():
    eco_terms, sec_terms = load_terms()
    results = defaultdict(lambda: {"total": 0, "eco": 0, "sec": 0, "mixed": 0})

    # alle JSON-Dateien unter data/raw/drucksache durchgehen
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for doc in data.get("documents", []):
                # Jahr aus dem Dokumentdatum
                year = "unbekannt"
                datum = doc.get("datum")
                if datum and len(datum) >= 4:
                    year = datum[:4]

                title = doc.get("titel", "")
                if not title:
                    continue
                title = title.lower()

                eco_hit = any(term in title for term in eco_terms)
                sec_hit = any(term in title for term in sec_terms)

                results[year]["total"] += 1

                if eco_hit and sec_hit:
                    results[year]["mixed"] += 1
                elif eco_hit:
                    results[year]["eco"] += 1
                elif sec_hit:
                    results[year]["sec"] += 1

    # Ausgabe
    total_docs = sum(v["total"] for v in results.values())
    print(f"\nGesamtzahl Dokumente: {total_docs}\n")
    print("Pro Jahr:")
    for year in sorted(results.keys()):
        r = results[year]
        print(
            f"{year}: total={r['total']}, eco={r['eco']}, sec={r['sec']}, mixed={r['mixed']}"
        )


if __name__ == "__main__":
    analyze_documents()
