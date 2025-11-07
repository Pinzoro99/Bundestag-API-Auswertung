# 01 – Data Source (Bundestag DIP API)

**Ziel:**
Abruf von Bundestagsdokumenten, die politische Themensetzungen abbilden, um die **Klassifikation der Dokumententitel** in vier Kategorien (Ökologie/Nachhaltigkeit, Sicherheit/Resilienz, Mixed, None) und deren **zeitliche Entwicklung** zu analysieren.

---

## API-Dokumentation

- Offizielle Dokumentation: [https://search.dip.bundestag.de/api/v1/swagger-ui/#/](https://search.dip.bundestag.de/api/v1/swagger-ui/#/)
- Hintergrundinfos: [https://dip.bundestag.de/über-dip/hilfe/api](https://dip.bundestag.de/über-dip/hilfe/api)

**Basis-URL:**
https://search.dip.bundestag.de/api/v1

---

## Zu verwendende Endpunkte

- **`/drucksache`** – **Die einzige Hauptquelle**. Sie liefert den Titel (`titel`) und Metadaten (`datum`, `urheber`) für die Klassifikation.
- **`/vorgang` – Wird für die primäre Analyse NICHT verwendet.** Die ausschließliche Konzentration auf `/drucksache` stellt die Trennschärfe der Titelanalyse sicher.

---

## Zeitraum

Die Datenabfragen sollen Dokumente vom **2019-01-01** bis zum **aktuellen Datum** (zunächst 2025-11-03) abdecken.
Der Zeitraum wird in der Datei `config/settings.json` unter dem Schlüssel `date_range` definiert und soll von den Skripten dynamisch gelesen werden.

---

## Abrufstrategie

- Paginierung über `cursor`
- Maximale Anzahl pro Request: `rows = 100`
- Filterung nach Zeitraum über API-Parameter (z. B. `f.datum.start`, `f.datum.end`)
- Zwischenspeicherung der Rohdaten als JSON unter `data/raw/` (eine Datei pro API-Request oder pro Jahr)

---

## Authentifizierung

- Die Bundestags-DIP-API ist öffentlich zugänglich.
- API-Key (laut offizieller Doku) wird als Parameter oder Header übergeben.
- Name der Umgebungsvariable: `DIP_API_KEY`
- Beispiel für `.env.example`: DIP_API_KEY=OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw
