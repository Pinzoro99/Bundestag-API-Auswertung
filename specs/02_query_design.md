# 02 – Query Design

**Ziel:**  
Untersuchung der quantitativen Entwicklung zentraler Begriffe in Bundestagsdokumenten von 2019 bis 2025, um zu erkennen, ob sich thematische Prioritäten von ökologischen und nachhaltigen Themen hin zu sicherheits- und resilienzbezogenen Themen verschieben.

---

## Überblick

Diese Datei beschreibt die geplante Abfragelogik und Verarbeitung der Bundestags-DIP-API-Daten.  
Ziel ist **nicht** die inhaltliche Klassifikation einzelner Dokumente, sondern die **Ermittlung der Häufigkeit und Entwicklung spezifischer Begriffe und Themencluster** über den Zeitverlauf.

---

## Schritt 1 – Datenerhebung

1. Abfrage der Endpunkte `/drucksache` und `/vorgang` für den Zeitraum **2019–2025**.  
2. Speicherung der Ergebnisse als JSON-Dateien unter `data/raw/` (eine Datei pro Jahr oder pro API-Seite).  
3. Verwendung des Parameters `cursor` zur Paginierung.  
4. API-Key über Umgebungsvariable `DIP_API_KEY`.  
5. Relevante Felder werden in `specs/03_field_mapping.md` definiert.

---

## Schritt 2 – Zusammenführung der Daten

- Zusammenführen von `/drucksache` und `/vorgang` über die gemeinsame `vorgangsId`.  
- Extraktion der relevanten Textfelder:
  - `titel`
  - `abstract`
  - `schlagwort`
  - `sachgebiet`
- Bildung eines kombinierten Textfeldes je Dokument:
  ```text
  text = titel + " " + abstract + " " + join(schlagwort) + " " + join(sachgebiet)
  ```
- Speicherung als strukturierte JSON- oder CSV-Datei (`data/processed/combined_texts.json`).

---

## Schritt 3 – Keyword-Frequenzanalyse

1. Laden der Keyword-Liste aus `data/term_list.json`.  
   Die Liste enthält zwei Cluster:
   - `oekologie_nachhaltigkeit`
   - `sicherheit_resilienz`
2. Für jedes Jahr:
   - Zählen, wie häufig **jedes einzelne Keyword oder eine seiner Varianten** in den Textfeldern vorkommt.  
   - Aggregation der Häufigkeiten je Cluster und Jahr.
3. Ergebnisse speichern in einer tabellarischen Struktur, z. B.:

| Jahr | Begriff | Cluster | Häufigkeit |
|------|----------|----------|-------------|
| 2019 | Nachhaltigkeit | oekologie_nachhaltigkeit | 284 |
| 2019 | Resilienz | sicherheit_resilienz | 15 |
| 2020 | Klimaschutz | oekologie_nachhaltigkeit | 312 |
| 2020 | Versorgungssicherheit | sicherheit_resilienz | 47 |

4. Optional: Berechnung relativer Häufigkeiten (z. B. Anteil pro 1.000 Wörter oder pro 100 Dokumente).

---

## Schritt 4 – Zeitreihenanalyse

- Aggregation der jährlichen Summen pro Cluster:
  ```text
  sum_oeko[year] = Σ(freq of all oekologie_nachhaltigkeit terms)
  sum_resi[year] = Σ(freq of all sicherheit_resilienz terms)
  ```
- Darstellung als Zeitreihe:
  - Entwicklung der absoluten Häufigkeiten (z. B. Liniengrafik)
  - Verhältnisindikator:  
    **Rₜ = (Summe Resilienz/Sicherheit) ÷ (Summe Nachhaltigkeit/Ökologie)**
  - Ein Rₜ > 1 zeigt eine relative Dominanz der Resilienz-/Sicherheitssemantik in diesem Jahr.

---

## Schritt 5 – Ergebnisstruktur

Die Resultate sollen unter `data/results/` abgelegt werden:

```text
data/
 ├─ raw/
 ├─ processed/
 │   └─ combined_texts.json
 └─ results/
     ├─ yearly_keyword_counts.csv
     ├─ yearly_cluster_sums.csv
     └─ relative_ratios.csv
```

---

## Schritt 6 – Erweiterbarkeit

- Weitere Cluster können ergänzt werden (z. B. „Wirtschaft“, „Soziales“, „Gesundheit“).  
- Eine spätere qualitative Kontextanalyse (z. B. Kookkurrenzen oder Satzebene) kann auf Basis derselben Daten erfolgen.  
- Optional: Integration von Stemming/Lemmatisierung zur robusteren Worterkennung.

---

## Fazit

Diese Pipeline dient der **deskriptiven Analyse politischer Themensetzung** im Bundestag, gemessen an der **zeitlichen Frequenz und semantischen Entwicklung definierter Schlüsselbegriffe**.  
Die Dokumente selbst werden **nicht klassifiziert**, sondern als Textträger für die Erfassung thematischer Trends verwendet.





  
