# 02 – Query Design (Optimiert für Dokumenten-Klassifikation)

**Ziel:**
Untersuchung der **Verbreitung** von ökologisch-nachhaltigen sowie versorgungs- und resilienzbezogenen Themen in Bundestags-Drucksachen (Titel-Ebene) von 2019 bis 2025. Die Analyse soll feststellen, ob sich thematische Prioritäten in den Dokumenten verschieben (gemessen am Anteil der Kategorien 'sec_hit', 'mixed' und 'eco_hit').

---

## Überblick

Diese Datei beschreibt die geplante Abfragelogik und Verarbeitung. Das zentrale Ziel ist die **eindeutige Klassifikation jedes Dokuments** anhand seines Titels in eine von vier Kategorien.

---

## Schritt 1 – Datenerhebung

1. Abfrage des Endpunkts **`/drucksache`** für den Zeitraum **2019–2025**. (Der Endpunkt `/vorgang` wird nicht mehr benötigt).
2. Speicherung der Rohdaten als JSON-Dateien unter `data/raw/` (eine Datei pro Jahr oder pro API-Seite).
3. Verwendung des Parameters `cursor` zur Paginierung.
4. API-Key über Umgebungsvariable `DIP_API_KEY`.
5. Nur die **minimalen Felder** (`id`, `datum`, `titel`, `typ`, `urheber`) werden gemäß `specs/03_field_mapping.md` extrahiert.

---

## Schritt 2 – Datenaufbereitung (Fokus auf Titel)

1. **Kein Zusammenführen von Drucksache und Vorgang.** Die Daten sind bereits in den Drucksachen enthalten.
2. **Extraktion und Bereinigung des Titels:** Für jedes Dokument wird nur das Feld **`titel`** extrahiert.
3. Der Titel-String wird zur Analyse in **Kleinbuchstaben** konvertiert.
4. Speicherung der bereinigten Daten mit den relevanten Metadaten als strukturierte JSON- oder CSV-Datei (`data/processed/processed_documents.csv`).

---

## Schritt 3 – Dokumenten-Klassifikation (Kernanalyse)

1. Laden der Keyword-Liste aus `data/term_list.json` (Cluster: `oekologie_nachhaltigkeit` und `sicherheit_resilienz`).
2. Für **jedes Dokument** (Titel):
    - Prüfen, ob **mindestens ein** Ökologie-Keyword enthalten ist (`eco_found` = True/False).
    - Prüfen, ob **mindestens ein** Resilienz-Keyword enthalten ist (`sec_found` = True/False).
3. **Zuweisung der finalen Kategorie** anhand der Booleans:
    - **`mixed`**: `eco_found` AND `sec_found`
    - **`eco_hit`**: `eco_found` AND NOT `sec_found`
    - **`sec_hit`**: NOT `eco_found` AND `sec_found`
    - **`none`**: NOT `eco_found` AND NOT `sec_found`
4. Speicherung einer Tabelle mit **Dokumenten-ID, Datum und zugeordneter Kategorie**.

---

## Schritt 4 – Zeitreihenanalyse (Aggregation der Verbreitung)

1. Aggregation der Ergebnisse nach **Jahr und Kategorie**.
2. **Zeitreihen-Datenpunkt:** Die zentrale Metrik ist die **Anzahl der Dokumente pro Kategorie und Jahr**.
3. Darstellung als Zeitreihe:
    - Entwicklung der absoluten Anzahl der Dokumente je Kategorie (Liniengrafik).
    - **Anteil-Analyse:** Entwicklung des **prozentualen Anteils** von `mixed` und `sec_hit` an allen Themen-Dokumenten (`mixed` + `eco_hit` + `sec_hit`) pro Jahr.

---

## Schritt 5 – Ergebnisstruktur

Die Resultate sollen unter `data/results/` abgelegt werden:

```text
data/
 ├─ raw/
 ├─ processed/
 │   └─ processed_documents.csv (Titel, Datum, Metadaten)
 └─ results/
     ├─ classified_documents.csv (Dokument-ID, Datum, final_category)
     └─ yearly_category_counts.csv (Jahr, eco_hit_count, sec_hit_count, mixed_count, none_count)


  
