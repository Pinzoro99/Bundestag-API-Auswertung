"""
analyze_terms.py
----------------
Analysiert die Titel der abgerufenen Drucksachen (data/raw/drucksache)
und prüft, ob sie Begriffe aus den Themenclustern
- Ökologie/Nachhaltigkeit
- Versorgung/Resilienz
enthalten.

Die Begriffe werden aus data/term_list.json geladen.
Die Ergebnisse (Dokumenten-Klassifikation pro Jahr) werden als CSV gespeichert.
"""

import os
import json
from collections import defaultdict
import csv

# --- KONFIGURATION (Muss mit Ihrem Projektpfad übereinstimmen) ---
# Annahme: data/term_list.json wurde aus config/term_list.json verschoben,
# wie in Ihrem Query Design impliziert.
TERM_FILE = "data/term_list.json" 
DATA_PATH = "data/raw/drucksache"
RESULTS_PATH = "data/results/yearly_category_counts.csv"
# -----------------------------------------------------------------


def load_terms():
    """
    Liest die Begriffe aus der term_list.json.
    Kombiniert 'keywords' und 'aliases' und konvertiert alles in Kleinbuchstaben.
    """
    try:
        with open(TERM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[FEHLER] Die Datei '{TERM_FILE}' wurde nicht gefunden.")
        return [], []

    cats = data.get("categories", {})
    eco_block = cats.get("oekologie_nachhaltigkeit")
    sec_block = cats.get("sicherheit_resilienz")

    if eco_block is None or sec_block is None:
        print("[FEHLER] Erwartete Kategorien ('oekologie_nachhaltigkeit' oder 'sicherheit_resilienz') fehlen.")
        return [], []

    # Da Sie die 'aliases' in der letzten term_list entfernt hatten, können wir diese Zeilen vereinfachen.
    # Wir behalten die alte Struktur für Robustheit, falls Sie sie später hinzufügen.
    eco_terms = [t.lower() for t in eco_block.get("keywords", [])]
    sec_terms = [t.lower() for t in sec_block.get("keywords", [])]

    print(f"[INFO] {len(eco_terms)} Ökologie/Nachhaltigkeit-Begriffe geladen.")
    print(f"[INFO] {len(sec_terms)} Sicherheit/Resilienz-Begriffe geladen.")
    return eco_terms, sec_terms


def analyze_documents():
    """
    Durchläuft alle Rohdaten-JSONs, liest die Titel und klassifiziert sie pro Jahr
    in die Kategorien eco, sec, mixed.
    """
    eco_terms, sec_terms = load_terms()
    
    if not eco_terms and not sec_terms:
        print("[FEHLER] Keine Suchbegriffe geladen. Analyse abgebrochen.")
        return

    # Initialisierung der Zähler: defaultdict(dict) für Jahr -> Kategorien
    results = defaultdict(lambda: {"total": 0, "eco": 0, "sec": 0, "mixed": 0, "none": 0})
    total_docs_processed = 0

    print(f"\n[INFO] Starte Analyse der Dokumente in {DATA_PATH}...")
    
    # Durchgehen aller JSON-Dateien unter data/raw/drucksache
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue
            
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"[WARNUNG] Fehler beim Lesen/Parsen von {path}: {e}")
                continue

            # Die API liefert die Drucksachen typischerweise unter dem Schlüssel 'documents'
            for doc in data.get("documents", []):
                
                # --- DATENEXTRAKTION ---
                datum = doc.get("datum")
                title = doc.get("titel", "")
                
                # Jahr aus dem Dokumentdatum extrahieren
                year = None
                if datum and len(datum) >= 4:
                    year = datum[:4]

                if not year or not title:
                    # Dokumente ohne Titel oder Datum werden ignoriert
                    continue 

                title_processed = title.lower()
                total_docs_processed += 1
                
                # --- KLASSIFIKATION ---
                # Substring-Suche (any() ist effizient)
                eco_hit = any(term in title_processed for term in eco_terms)
                sec_hit = any(term in title_processed for term in sec_terms)

                # Zuweisung der finalen Kategorie (Priorisierung der Mixed-Kategorie)
                category_key = "none"
                
                if eco_hit and sec_hit:
                    category_key = "mixed"
                elif eco_hit:
                    category_key = "eco"
                elif sec_hit:
                    category_key = "sec"
                # else: category_key bleibt "none"

                # Zähler aktualisieren
                results[year]["total"] += 1
                results[year][category_key] += 1
                
    
    # --- ERGEBNIS-VERARBEITUNG ---
    print("\n[INFO] Analyse abgeschlossen.")
    print(f"Gesamtzahl analysierter Dokumente: {total_docs_processed}\n")
    
    # Speichern und Ausgabe der Ergebnisse
    save_and_print_results(results)


def save_and_print_results(results):
    """Speichert die Ergebnisse in einer CSV-Datei und gibt sie auf der Konsole aus."""
    
    # Daten für CSV vorbereiten und nach Jahr sortieren
    data_to_save = [
        {"year": year, **results[year]}
        for year in sorted(results.keys())
    ]

    fieldnames = ["year", "total", "eco", "sec", "mixed", "none"]

    # Sicherstellen, dass der Ausgabeordner existiert
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    
    # Speichern der Ergebnisse
    try:
        with open(RESULTS_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_save)
            
        print(f"[INFO] Ergebnisse gespeichert unter: {RESULTS_PATH}\n")
    except IOError as e:
        print(f"[FEHLER] Konnte Ergebnisse nicht speichern: {e}")

    # Konsolenausgabe
    print("--- Klassifikationsergebnisse pro Jahr ---")
    print(f"{'Jahr':<6} | {'Total':<6} | {'Eco':<6} | {'Sec':<6} | {'Mixed':<6} | {'None':<6}")
    print("-" * 43)
    for year in sorted(results.keys()):
        r = results[year]
        print(f"{year:<6} | {r['total']:<6} | {r['eco']:<6} | {r['sec']:<6} | {r['mixed']:<6} | {r['none']:<6}")


if __name__ == "__main__":
    analyze_documents()
