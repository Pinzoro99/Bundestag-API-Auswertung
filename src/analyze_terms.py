import json
import os
import re
from pathlib import Path
from datetime import datetime

# Ordner mit den heruntergeladenen Drucksachen
RAW_DIR = Path("data/raw/drucksache")

# Ausgabeordner
RESULTS_DIR = Path("data/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Suchmuster (sehr grob, kannst du später fein machen)
ECO_TERMS = [
    r"klima", r"klimaschutz", r"klimakonferenz", r"umwelt",
    r"nachhaltig", r"naturschutz", r"energie", r"biodiversität"
]

SEC_TERMS = [
    r"sicherheits", r"sicherheit", r"cyber", r"resilienz",
    r"kritische anlage", r"kritische infrastr", r"zivile sicherheit",
    r"krisenlage", r"abwehr"
]

def match_any(patterns, text):
    text_l = text.lower()
    for pat in patterns:
        if re.search(pat, text_l):
            return True
    return False

def main():
    eco_count = 0
    sec_count = 0
    total_docs = 0

    # optional: nach Jahr gruppieren
    per_year = {}

    for json_file in RAW_DIR.glob("*.json"):
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        documents = data.get("documents", [])
        for doc in documents:
            total_docs += 1
            title = doc.get("titel") or ""
            datum = doc.get("datum") or ""
            # Jahr rausziehen
            year = None
            if datum:
                try:
                    year = datetime.fromisoformat(datum).year
                except ValueError:
                    # manchmal nur YYYY-MM-DD → geht auch
                    try:
                        year = datetime.strptime(datum, "%Y-%m-%d").year
                    except ValueError:
                        year = None

            is_eco = match_any(ECO_TERMS, title)
            is_sec = match_any(SEC_TERMS, title)

            # global zählen
            if is_eco:
                eco_count += 1
            if is_sec:
                sec_count += 1

            # pro Jahr zählen
            if year:
                if year not in per_year:
                    per_year[year] = {"eco": 0, "sec": 0, "total": 0}
                per_year[year]["total"] += 1
                if is_eco:
                    per_year[year]["eco"] += 1
                if is_sec:
                    per_year[year]["sec"] += 1

    # einfache Textausgabe
    print("Gesamtzahl Dokumente:", total_docs)
    print("Treffer Ökologie/Nachhaltigkeit:", eco_count)
    print("Treffer Sicherheit/Resilienz:", sec_count)
    print()
    print("Pro Jahr:")
    for year in sorted(per_year.keys()):
        y = per_year[year]
        print(f"{year}: total={y['total']}, eco={y['eco']}, sec={y['sec']}")

    # zusätzlich als CSV speichern
    csv_path = RESULTS_DIR / "term_counts_by_year.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("year,total,eco,sec\n")
        for year in sorted(per_year.keys()):
            y = per_year[year]
            f.write(f"{year},{y['total']},{y['eco']},{y['sec']}\n")

    print(f"\nErgebnisse gespeichert unter: {csv_path}")

if __name__ == "__main__":
    main()

