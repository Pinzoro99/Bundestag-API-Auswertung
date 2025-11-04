# Bundestag Themenanalyse 2019–2025  
### Wandel politischer Diskurse von Nachhaltigkeit/Ökologie zu Sicherheit/Resilienz

---

## 🧭 Projektbeschreibung

Dieses Repository dient der Untersuchung, **ob und in welchem Ausmaß sich politische Diskurse im Deutschen Bundestag zwischen 2019 und 2025 verschoben haben** –  
von **ökologisch-nachhaltigen Themen** (z. B. Klimaschutz, Nachhaltigkeit, Energiewende) hin zu **Sicherheits- und Resilienzthemen** (z. B. Versorgungssicherheit, Krisenfestigkeit, Verteidigung).

Die Analyse basiert auf einer quantitativen **Frequenzanalyse von Begriffen in Bundestagsdokumenten**, die über die offizielle **DIP-API** (Dokumentations- und Informationssystem für Parlamentarische Vorgänge) abgerufen werden.

Das Projekt ist Teil einer Masterarbeit im Bereich *Risiko- und Krisenkommunikation / Agrar- und Umweltpolitik*  
und orientiert sich an wissenschaftlichen Ansätzen von u. a. **Peter H. Feindt** und anderen Forschern,  
die eine Verschiebung politischer Prioritäten hin zu „Resilienz- und Sicherheitslogiken“ in gesellschaftlichen Diskursen postulieren.

---

## 🎯 Zielsetzung

- Quantitative Erfassung der **Häufigkeit zentraler Begriffe** aus zwei Themenclustern:
  1. **Ökologie & Nachhaltigkeit**
  2. **Sicherheit & Resilienz**

- Erstellung einer **Zeitreihe (2019–2025)**, um thematische Trends und potenzielle Verschiebungen sichtbar zu machen.

- Grundlage für eine spätere **Diskursanalyse** oder **semantische Kontextauswertung**.

---

## 🧩 Methodisches Vorgehen

1. **Datenerhebung:**  
   Abruf von Bundestags-Dokumenten über die offizielle [DIP-API](https://search.dip.bundestag.de/api/v1/swagger-ui/#/),  
   insbesondere der Endpunkte `/drucksache` und `/vorgang`.

2. **Verarbeitung:**  
   Zusammenführung und Bereinigung der Daten, Bildung kombinierter Textfelder aus Titel, Abstract, Schlagwörtern und Sachgebieten.

3. **Analyse:**  
   Zählung definierter Begriffe (aus `data/term_list.json`) pro Jahr und Themencluster.  
   Ergebnis: relative und absolute Häufigkeiten + Verhältnisindikator (Rₜ).

4. **Visualisierung (optional):**  
   Darstellung der zeitlichen Entwicklung über Linien- oder Balkendiagramme.

---

## 📁 Repository-Struktur

```text
project-root/
 ├─ config/
 │   └─ settings.json         # Basis-URL, Endpunkte, Zeitraum, API-Key-Handling
 │
 ├─ data/
 │   ├─ raw/                  # Rohdaten aus der DIP-API
 │   ├─ processed/            # Bereinigte und kombinierte Textdaten
 │   ├─ results/              # Analysedaten (Keyword-Counts, Zeitreihen, etc.)
 │   └─ term_list.json        # Keyword-Cluster für die Themenanalyse
 │
 ├─ logs/
 │   └─ api_fetch.log         # Log-Dateien der API-Abfragen
 │
 ├─ specs/                    # Methodische & technische Spezifikationen
 │   ├─ 01_data_source.md
 │   ├─ 02_query_design.md
 │   └─ 03_field_mapping.md
 │
 ├─ src/                      # Skripte zur Ausführung der Pipeline
 │   ├─ fetch_data.py
 │   ├─ process_data.py
 │   ├─ analyze_terms.py
 │   ├─ utils.py
 │   └─ README.md
 │
 └─ README.md                 # (dieses Dokument)
```

---

## ⚙️ Funktionsweise (Pipeline)

| Schritt | Datei | Beschreibung |
|----------|--------|--------------|
| 1️⃣ Datenabruf | `src/fetch_data.py` | Holt Bundestagsdokumente über die DIP-API und speichert sie unter `data/raw/`. |
| 2️⃣ Verarbeitung | `src/process_data.py` | Extrahiert relevante Felder, kombiniert Texte, schreibt Ergebnis nach `data/processed/`. |
| 3️⃣ Analyse | `src/analyze_terms.py` | Zählt Keywords je Jahr und Cluster, erzeugt Zeitreihen und Verhältnisindikator. |
| 🔧 Hilfen | `src/utils.py` | Logging, File Handling, JSON-/CSV-Operationen. |

---

## 🧠 Analyseindikator

**Verhältnisindikator Rₜ:**

\[
Rₜ = \frac{\text{Summe Resilienz/Sicherheit}}{\text{Summe Nachhaltigkeit/Ökologie}}
\]

Ein Rₜ > 1 deutet auf eine stärkere thematische Dominanz von Sicherheits- und Resilienzbegriffen hin.

---

## 🧰 Voraussetzungen

- Python 3.9+  
- Bibliotheken: `requests`, `pandas`, `dotenv` (optional für API-Key-Handling)  
- Aktiver DIP-API-Key (öffentlich zugänglich, siehe [API-Hilfe](https://dip.bundestag.de/über-dip/hilfe/api))

---

## 🚀 Nutzung (Beispiel-Workflow)

```bash
# 1. Repository klonen
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# 2. API-Key setzen
echo "DIP_API_KEY=DEIN_KEY" > .env

# 3. Daten abrufen
python src/fetch_data.py

# 4. Daten verarbeiten
python src/process_data.py

# 5. Analyse durchführen
python src/analyze_terms.py
```

---

## 🧾 Lizenz & Hinweise

Dieses Repository dient wissenschaftlichen Zwecken.  
Die Bundestags-Daten stammen aus dem öffentlichen [Dokumentations- und Informationssystem (DIP)](https://dip.bundestag.de/).  
Die Nutzung erfolgt gemäß den dort angegebenen Bestimmungen.

---


