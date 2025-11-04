# 01 – Data Source (Bundestag DIP API)

**Ziel:**  
Abruf von Bundestagsdokumenten, die politische Themensetzungen abbilden, für eine Diskursverschiebungsanalyse (Ökologie/Nachhaltigkeit → Sicherheit/Resilienz).

---

## API-Dokumentation

- Offizielle Dokumentation: [https://search.dip.bundestag.de/api/v1/swagger-ui/#/](https://search.dip.bundestag.de/api/v1/swagger-ui/#/)
- Hintergrundinfos: [https://dip.bundestag.de/über-dip/hilfe/api](https://dip.bundestag.de/über-dip/hilfe/api)

**Basis-URL:**
https://search.dip.bundestag.de/api/v1

---

## Zu verwendende Endpunkte

- `/drucksache` – Hauptquelle für inhaltliche Titel, Abstracts, Schlagwörter und Datumsangaben  
- `/vorgang` – Kontextquelle für dieselben Zeiträume; liefert zusätzliche Schlagwörter, Sachgebiete und Initiatoren

Andere Endpunkte (z. B. `/plenarprotokoll`, `/aktivitaet`) sind optional und werden in dieser Version nicht berücksichtigt.

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

---

## Erwartete Rückgabefelder (Beispiele)

**Drucksache (Beispiel):**
```json
{
"drucksacheId": "12345",
"vorgangsId": "9876",
"titel": "Gesetz zur Stärkung der Versorgungssicherheit",
"abstract": "Die Bundesregierung berichtet über Maßnahmen zur Energieversorgung...",
"datum": "2023-02-14",
"typ": "Große Anfrage",
"urheber": ["Fraktion Bündnis 90/Die Grünen"],
"sachgebiet": ["Energie", "Landwirtschaft"],
"schlagwort": ["Versorgungssicherheit", "Klimaschutz"]
}

Vorgang (Beispiel):
json
{
  "vorgangsId": "9876",
  "vorgangstyp": "Gesetzgebung",
  "titel": "Gesetz zur Stärkung der Resilienz der Landwirtschaft",
  "initiative": ["Bundesregierung"],
  "aktualisiert": "2023-05-14",
  "sachgebiet": ["Umwelt", "Landwirtschaft"],
  "schlagwort": ["Resilienz", "Nachhaltigkeit"],
  "legislaturperiode": 20
}

