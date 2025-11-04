# Projektstruktur & Skript-Übersicht (`src/README.md`)

**Ziel:**  
Dieser Ordner enthält alle Skripte zur Abfrage, Verarbeitung und Analyse der Bundestags-DIP-Daten.  
Die Skripte basieren auf den Spezifikationen in `/specs/` und nutzen die Einstellungen aus `/config/settings.json`.

---

## 📂 Empfohlene Ordnerstruktur

```text
project-root/
 ├─ config/
 │   └─ settings.json
 │
 ├─ data/
 │   ├─ raw/            # Original-JSON-Dateien aus der API (eine Datei pro Jahr oder pro API-Request)
 │   ├─ processed/      # Bereinigte und kombinierte Textdaten
 │   ├─ results/        # Ergebnisdaten (Keyword-Counts, Zeitreihen, etc.)
 │   └─ term_list.json  # Keyword-Cluster (Ökologie/Nachhaltigkeit vs. Sicherheit/Resilienz)
 │
 ├─ logs/
 │   └─ api_fetch.log   # Log-Dateien der API-Abfragen
 │
 ├─ specs/
 │   ├─ 01_data_source.md
 │   ├─ 02_query_design.md
 │   └─ 03_field_mapping.md
 │
 ├─ src/
 │   ├─ README.md        # (dieses Dokument)
 │   ├─ fetch_data.py    # Holt Daten aus der Bundestags-DIP-API und speichert sie unter /data/raw/
 │   ├─ process_data.py  # Kombiniert / bereinigt Daten laut field_mapping.md
 │   ├─ analyze_terms.py # Führt Keyword-Frequenz- und Zeitreihenanalysen durch
 │   └─ utils.py         # Hilfsfunktionen (Logging, File Handling, Text Cleaning, etc.)
 │
 └─ .env.example         # Beinhaltet: DIP_API_KEY=DEIN_KEY
```

---

## 🧩 Skriptbeschreibung

| Datei | Funktion |
|-------|-----------|
| **fetch_data.py** | Führt die API-Requests aus, nutzt die Parameter aus `settings.json`, speichert Antworten in `data/raw/`. |
| **process_data.py** | Führt die beiden Endpunkte (`/drucksache` und `/vorgang`) zusammen, bereinigt Felder, erstellt kombinierte Textfelder. |
| **analyze_terms.py** | Lädt die verarbeiteten Texte und zählt die Keywords aus `data/term_list.json` pro Jahr und Cluster. Ergebnisse werden in `data/results/` gespeichert. |
| **utils.py** | Enthält gemeinsame Funktionen (z. B. Logging, Datumsparser, Textnormalisierung, JSON-Handling). |

---

## 🧠 Ablauf (Pipeline-Logik)

1. **fetch_data.py** → ruft Daten ab und speichert Rohdaten.  
2. **process_data.py** → bereitet sie auf und kombiniert relevante Textfelder.  
3. **analyze_terms.py** → zählt Keywords, erstellt Zeitreihen und Verhältnisindikatoren.  
4. Ergebnisse → in `data/results/` gespeichert, optional Visualisierung.

---

## 🔧 ToDo / Nächste Schritte

- Erstellung der Skripte (Codex oder manuell)
- Implementierung der Keyword-Zählung und Zeitreihenaggregation
- Erweiterung der Cluster in `data/term_list.json` bei Bedarf

---

**Hinweis:**  
Die Skripte sollen modular aufgebaut werden – d. h. jede Komponente (`fetch`, `process`, `analyze`) kann unabhängig ausgeführt werden.  
Alle Pfade und Parameter werden dynamisch aus `config/settings.json` gelesen.
