# 03 – Field Mapping

**Ziel:**  
Festlegen, welche Felder aus den DIP-API-Responses (`/drucksache` und `/vorgang`) extrahiert werden sollen und unter welchen Namen sie im Projekt weiterverwendet werden.  
Die Feld-Auswahl ist darauf ausgerichtet, Textbestandteile für eine spätere Frequenzanalyse zusammenzuführen (Titel, Abstract, Schlagwörter, Sachgebiete) und Dokumente ggf. über `vorgangsId` zu verknüpfen.

---

## 1. Allgemeine Regeln

1. Wenn ein Feld in der API verschachtelt ist (z. B. `vorgangsbezug.id`), soll es beim Parsen in ein **flaches Feld** umgewandelt werden (z. B. `vorgangsId`).
2. Listenfelder (z. B. `schlagworte`, `sachgebiete`) sollen als **Liste** erhalten bleiben oder zu einem String mit Trennzeichen (z. B. `"; "`) zusammengeführt werden – je nach späterer Implementierung.
3. Alle Felder, die Text enthalten, sollen für die spätere Analyse in ein gemeinsames Textfeld aufgenommen werden können (siehe `specs/02_query_design.md`, Schritt 2).
4. Felder, die nur für Metadaten gebraucht werden (z. B. Datum), sollen im Rohformat übernommen werden.

---

## 2. Mapping für `/drucksache`

**Eingang:** Response eines Calls auf  
`GET https://search.dip.bundestag.de/api/v1/drucksache`

**Zu extrahierende Felder:**

| API-Feld (Quelle)          | Zielname im Projekt | Beschreibung |
|----------------------------|---------------------|--------------|
| `id`                       | `drucksacheId`      | eindeutige ID der Drucksache |
| `vorgangsbezug.id`         | `vorgangsId`        | Referenz auf zugehörigen Vorgang (falls vorhanden) |
| `titel`                    | `titel`             | Haupttitel der Drucksache |
| `abstract`                 | `abstract`          | Kurzbeschreibung/Zusammenfassung |
| `datum`                    | `datum`             | Veröffentlichungs- bzw. Erstellungsdatum |
| `typ`                      | `typ`               | Art der Drucksache (z. B. Kleine Anfrage, Gesetzentwurf) |
| `urheber`                  | `urheber`           | einreichende Stelle (Fraktion, Bundesregierung usw.) |
| `sachgebiete`              | `sachgebiet`        | thematische Zuordnung lt. Bundestag |
| `schlagworte`              | `schlagwort`        | inhaltliche Verschlagwortung |

**Hinweise:**

- Wenn `vorgangsbezug` nicht vorhanden ist, bleibt `vorgangsId` leer.
- `sachgebiete` und `schlagworte` können als Liste oder als zusammengeführter String gespeichert werden.
- `titel`, `abstract`, `schlagwort` und `sachgebiet` sollen später für das kombinierte Textfeld verwendet werden.

---

## 3. Mapping für `/vorgang`

**Eingang:** Response eines Calls auf  
`GET https://search.dip.bundestag.de/api/v1/vorgang`

**Zu extrahierende Felder:**

| API-Feld (Quelle)  | Zielname im Projekt | Beschreibung |
|--------------------|---------------------|--------------|
| `id`               | `vorgangsId`        | eindeutige ID des Vorgangs |
| `vorgangstyp`      | `vorgangstyp`       | Art des Vorgangs (Gesetzgebung, Antrag, Bericht …) |
| `titel`            | `titel`             | Bezeichnung des Vorgangs |
| `initiative`       | `initiative`        | einreichende Stelle (z. B. Bundesregierung, Fraktion) |
| `sachgebiete`      | `sachgebiet`        | thematische Zuordnung |
| `schlagworte`      | `schlagwort`        | inhaltliche Verschlagwortung |
| `aktualisiert`     | `aktualisiert`      | letztes Änderungs-/Aktualisierungsdatum |
| `legislaturperiode`| `legislaturperiode` | Zuordnung zur Wahlperiode |

**Hinweise:**

- `titel`, `schlagwort` und `sachgebiet` sollen ebenfalls in das kombinierte Textfeld einfließen.
- Wenn sowohl Drucksache als auch Vorgang vorhanden sind, kann der Titel aus der Drucksache bevorzugt werden (abhängig von Implementierung).

---

## 4. Kombiniertes Textfeld

Für die spätere Frequenzanalyse soll aus den oben genannten Feldern ein gemeinsames Textfeld je Dokument gebildet werden, z. B.:

```text
text = titel + " " + abstract + " " + join(schlagwort) + " " + join(sachgebiet)
```

- Wenn `abstract` fehlt, wird es einfach weggelassen.
- Wenn `schlagwort` oder `sachgebiet` Listen sind, sollen sie mit einem Leerzeichen oder Semikolon verbunden werden.
- Dieses kombinierte Feld wird später von den Skripten in `src/` genutzt, um die Begriffe aus `data/term_list.json` zu zählen.

---

## 5. Datum / Zeitliche Zuordnung

Für die spätere Aggregation nach Jahr wird **mindestens eines** der folgenden Felder benötigt:

1. Bei `/drucksache`: `datum`
2. Bei `/vorgang`: `aktualisiert`

Falls beide vorhanden sind, kann die Implementierung eine Priorität definieren (z. B. zuerst `datum`, sonst `aktualisiert`).  
Das Jahr wird daraus extrahiert und zur Gruppierung verwendet.

---

## 6. Ziel

Nach Anwendung dieses Field Mappings soll jedes Dokument (egal ob aus `/drucksache` oder `/vorgang`) mindestens folgende Felder aufweisen:

- `id` bzw. `drucksacheId` oder `vorgangsId`
- `titel`
- `text` (kombiniertes Textfeld, siehe oben)
- `datum` oder `aktualisiert` (zur Jahreszuordnung)
- optionale Metadaten: `typ`, `initiative`/`urheber`, `sachgebiet`, `schlagwort`

Diese einheitliche Struktur ermöglicht es den nachfolgenden Skripten, ohne weitere Sonderfälle eine Frequenzanalyse über mehrere Jahre durchzuführen.
