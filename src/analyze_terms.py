"""
analyze_terms.py
----------------
Analysiert die abgerufenen Bundestags-Dokumente (Drucksachen)
nach dem Vorkommen definierter Begriffe in den TITELN.

Verwendet:
- data/raw/drucksache/
- config/term_list.json
"""

import os
import json
from collections import defaultdict

DATA_PATH = "data/raw/drucksache"
TERM_FILE = "config/term_list.json"

def load_terms():
    try:
        with open(TERM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        eco_terms = [t.lower() for t in data["oekologie_nachhaltigkeit"]["keywords"]]
        sec_terms = [t.lower() for t in data["sicherheit_resilienz"]["keywords"]]
        print(f"✅ Begriffe aus {TERM_FILE} geladen.")
        return eco_terms, sec_terms
    except FileNotFoundError:
        print(f"⚠️  {TERM_FILE} nicht gefunden – verwende Fallback-Begriffe.")
        return ["klimaschutz", "nachhaltigkeit", "ökologie"], ["sicherheit", "resilienz"]

def analyze_documents():
    eco_terms, sec_terms = load_terms()
    results = defaultdict(lambda: {"total": 0, "eco": 0, "sec": 0, "mixed": 0})

    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for doc in data.get("documents", []):
                year = "unbekannt"
                if "datum" in doc and len(doc["datum"]) >= 4:
                    year = doc["datum"][:4]

                title = doc.get("titel", "").lower()
                if not title:
                    continue

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
    total_eco = sum(v["eco"] for v in results.values())
    total_sec = sum(v["sec"] for v in results.values())
    total_mixed = sum(v["mixed"] for v in results.values())

    print(f"\nGesamtzahl Dokumente: {total_docs}")
    print(f"Ökologie/Nachhaltigkeit: {total_eco}")
    print(f"Sicherheit/Resilienz: {total_sec}")
    print(f"Beide Themen (mixed): {total_mixed}\n")

    print("Pro Jahr:")
    for year, vals in sorted(results.items()):
        print(f"{year}: total={vals['total']}, eco={vals['eco']}, sec={vals['sec']}, mixed={vals['mixed']}")

if __name__ == "__main__":
    analyze_documents()
