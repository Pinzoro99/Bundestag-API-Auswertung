# Bundestag Themenanalyse 2019–2025  
### Wandel politischer Diskurse von Nachhaltigkeit/Ökologie zu Sicherheit/Resilienz

---

## 🧭 Projektbeschreibung

Dieses Repository dient der Untersuchung, **ob und in welchem Ausmaß sich politische Diskurse im Deutschen Bundestag zwischen 2019 und 2025 verschoben haben** –  
von **ökologisch-nachhaltigen Themen** hin zu **Sicherheits- und Resilienzthemen**.

Die Analyse basiert auf einer **quantitativen Klassifikation der Titel von Bundestagsdokumenten** (Drucksachen), die über die offizielle **DIP-API** abgerufen werden. Jedes Dokument wird einer von vier Kategorien zugeordnet: `sec_hit`, `eco_hit`, `mixed`, oder `none`.

---

## 🎯 Zielsetzung

- Quantitative Erfassung der **Verbreitung** von Dokumenten in den Kategorien:
  1. **Ökologie & Nachhaltigkeit** (`eco_hit`)
  2. **Sicherheit & Resilienz** (`sec_hit`)
  3. **Gemischt** (`mixed`)
  4. **Kein Treffer** (`none`)

- Erstellung einer **Zeitreihe (2019–2025)**, um thematische Trends und potenzielle Verschiebungen sichtbar zu machen.

- Berechnung eines Indikators, der die relative Dominanz der Sicherheitsthemen anzeigt.

---

## 🧩 Methodisches Vorgehen

1. **Datenerhebung:** Abruf von Bundestags-Drucksachen (Endpunkt **`/drucksache`**) über die [DIP-API](https://search.dip.bundestag.de/api/v1/swagger-ui/#/).

2. **Verarbeitung:** **Fokus auf den Titel** (`titel`); Bereinigung der Daten und Erstellung der minimalistischen Analyse-Tabelle.

3. **Analyse:** Zuweisung der Dokumentenkategorie **basierend nur auf Keyword-Treffern im Titel** (aus `data/term_list.json`). Aggregation der **Anzahl der Dokumente** pro Kategorie und Jahr.

4. **Visualisierung (optional):** Darstellung der zeitlichen Entwicklung über Linien- oder Balkendiagramme.

---

## 📁 Repository-Struktur

```text
project-root/
 ├─ config/
 │   └─ settings.json
 ├─ data/
 │   ├─ raw/
 │   ├─ processed/
 │   ├─ results/
 │   └─ term_list.json
 ├─ logs/
 ├─ specs/
 ├─ src/
 │   └─ main.py # Orchestriert die Pipeline
 └─ README.md   # (dieses Dokument)
