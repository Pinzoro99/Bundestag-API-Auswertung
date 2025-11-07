**Ziel:**
Festlegen der minimal benötigten Felder aus der DIP-API-Response (`/drucksache`), um die Titel für die Klassifikation in die Kategorien sec_only, eco_only, mixed und none zu nutzen.

---

## 1. Allgemeine Regeln (Angepasst)

1. Der Abruf erfolgt ausschließlich über den Endpunkt `/drucksache`.
2. Das **`titel`**-Feld ist die **einzige Datenquelle** für die Keyword-Analyse.
3. Andere Felder dienen lediglich der zeitlichen Zuordnung (`datum`) und als Metadaten (`typ`, `urheber`).

---

## 2. Mapping für `/drucksache`

**Eingang:** Response eines Calls auf `GET https://search.dip.bundestag.de/api/v1/drucksache`

**Zu extrahierende Felder:**

| API-Feld (Quelle) | Zielname im Projekt | Beschreibung | Relevanz |
| :--- | :--- | :--- | :--- |
| `id` | `drucksacheId` | eindeutige ID der Drucksache | Identifikation |
| `datum` | `datum` | Veröffentlichungsdatum | Zeitliche Zuordnung (Jahr) |
| **`titel`** | **`titel_raw`** | Haupttitel der Drucksache | **Basis für die Keyword-Analyse** |
| `typ` | `typ` | Art der Drucksache | Metadaten |
| `urheber` | `urheber` | einreichende Stelle | Metadaten |

---

## 3. Kombiniertes Textfeld (Wegfall)

Das Konzept des kombinierten Textfeldes **entfällt**. Die Analyse erfolgt direkt auf dem Feld `titel_raw`, nachdem es in Kleinbuchstaben konvertiert wurde (`titel_processed`).

---

## 4. Zielstruktur

Nach dem Parsen soll jeder Datensatz (Drucksache) mindestens folgende Felder aufweisen:
* `drucksacheId`
* `datum` (für Jahres-Extraktion)
* `titel_raw`
* `typ`
* `urheber`
