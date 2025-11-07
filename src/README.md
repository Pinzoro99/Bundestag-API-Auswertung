# Projektstruktur & Skript-Übersicht (`src/README.md`)

**Ziel:** Dieser Ordner enthält alle Skripte zur Orchestrierung, Abfrage, Verarbeitung und **Klassifikation** der Bundestags-DIP-Daten. Die Pipeline ist auf die Analyse der **Dokumenten-Titel** fokussiert.

---

## 🧩 Skriptbeschreibung

| Datei | Funktion | Details |
|-------|-----------|----------------------------------------------------|
| **main.py** | **Pipeline-Orchestrierung** | Steuert den gesamten Prozess: Initialisiert Logging, ruft nacheinander `fetch_data`, `process_data` und `analyze_terms` auf. |
| **fetch_data.py** | **Datenabruf** | Holt Dokumente über die DIP-API. **Ausschließlich** der Endpunkt `/drucksache` für den Zeitraum 2019–2025 wird verwendet. |
| **process_data.py** | **Datenvorbereitung** | Bereinigt die Rohdaten. **Extrahiert nur ID, Titel, Datum** aus den `/drucksache`-JSONs und speichert sie als `data/processed/processed_documents.csv`. |
| **analyze_terms.py** | **Klassifikation** | Führt die zentrale Analyse durch: **Klassifiziert jeden Titel** in `eco_hit`, `sec_hit`, `mixed`, oder `none` und aggregiert die Zähler pro Jahr in `data/results/`. |
| **utils.py** | **Hilfsfunktionen** | Stellt Logging, JSON- und CSV-Handling bereit. |

---

## 🧠 Ablauf (Pipeline-Logik)

Die Pipeline wird über **`main.py`** gestartet und führt folgende Schritte aus:

1.  **Datenbeschaffung:** `fetch_data.py` ruft die Rohdaten ab (`data/raw/`).
2.  **Datenreinigung:** `process_data.py` erstellt die minimale Analyse-CSV (`data/processed/`).
3.  **Analyse:** `analyze_terms.py` klassifiziert die Daten und speichert die finalen Zeitreihen-Zähler (`data/results/`).

---

## 🚀 Nutzung

Um die vollständige Analyse durchzuführen, führen Sie das Hauptskript im `src/` Verzeichnis aus:

```bash
python main.py
