# ods-utils-py
Mit `ods-utils-py` lässt sich direkt aus Python auf die Automation API von Opendatasoft zugreifen. Voraussetzung ist der Besitz eines gültigen API Schlüssels ([API-Schlüssel erstellen](#api-schlüssel-einrichten)). [Der Quellcode ist öffentlich auf Github](https://github.com/RenatoFarruggio/ods-utils-py).


## Inhaltsverzeichnis

   - [Installation](#installation)
   - [Voraussetzungen](#voraussetzungen)
   - [Erste Schritte](#erste-schritte)
     - [API-Schlüssel einrichten](#api-schlüssel-einrichten)
   - [Verwendung](#verwendung)
   - [Weiterführende Links](#weiterführende-links)
   - [Lizenz](#lizenz)

---

## Installation

Installation via `pip`:

```bash
pip install ods-utils-py
```

---

## Voraussetzungen

- **Python Version:** 3.11 oder höher
- **API-Schlüssel:** Ein gültiger API-Schlüssel von Opendatasoft

---

## Erste Schritte

### API-Schlüssel einrichten

Um `ods-utils-py` nutzen zu können, wird ein gültiger API-Key von Opendatasoft benötigt. 

[Für die OGD Basel kann der API Key hier erstellt werden](https://data.bs.ch/account/api-keys/).

Für die Key-Erstellung auf anderen Plattformen kann oben rechts auf die Schaltfläche mit dem Benutzernamen geklickt werden, um die Kontoeinstellungen zu öffnen. Unter API-Keys können benutzerdefinierte Keys mit den entsprechenden Berechtigungen erstellt werden. 

Der Name sollte beschreiben wofür er verwendet wird, beispielsweise `"ods_utils_py - <Initialer Name des Keys>"`

Der API Key benötigt die folgenden 4 Berechtigungen:
- Alle Datensätze durchsuchen
- Neue Datensätze erstellen
- Alle Datensätze bearbeiten
- Eigene Datensätze veröffentlichen

Der API Key wird nun als Umgebungsvariable benötigt.

### Umgebungsvariablen einrichten
Als nächstes müssen die Umgebungsvariablen definiert werden. Dafür sollte im Root-Verzeichnis eine `.env` Datei erstellt werden mit dem folgenden Inhalt, bzw. falls schon eine solche Datei existiert, die folgenden Zeilen ergänzt und ausgefüllt werden.

```text
ODS_API_KEY=your_api_key

PROXY_USER=your_proxy_user
PROXY_PASSWORD=your_proxy_password
PROXY_ADDRESS=your_proxy_address
PROXY_PORT=your_proxy_port

ODS_DOMAIN=data.bs.ch
ODS_API_TYPE=automation/v1.0
```

## Verwendung

Hier ein einfaches Beispiel, um die Anzahl der Datensätze abzurufen:

```python
import ods_utils_py as ods_utils

num_datasets = ods_utils.get_number_of_datasets()
print(f"Derzeit haben wir {num_datasets} Datensätze.")
```

Falls eine gewünschte Funktion nicht existiert, kann sie über _requests_utils implementiert werden:

```python
import ods_utils_py as ods_utils

antwort = ods_utils._requests_get("https://www.example.com")
print(antwort.text)
```

*Hinweis:* Die meisten dieser Funktionen sollten dann langfristig in `ods_utils_py` integriert werden.

---

## Weiterführende Links
Die vollständige Dokumentation der Automation API 1.0 ist [hier](https://help.opendatasoft.com/apis/ods-automation-v1/) zu finden.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE) Datei im Repository für den vollständigen Lizenztext.
