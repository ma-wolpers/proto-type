# ProtoType

**ProtoType** ist eine Lernumgebung, mit der verschiedene Aspekte der Kommunikation in digitalen Systemen (z.B. Kodierung, Adressierung, Nachrichtenübertragung) explorativ erarbeitet werden können. Das Programm ermöglicht mehreren Nutzer:innen, netzwerkartig auf einen gemeinsamen Binärstrom zuzugreifen und darüber Nachrichten auszutauschen.

## Voraussetzungen

- Python 3.6 oder neuer (empfohlen: Python 3.7+)
- Tkinter (meist vorinstalliert)

## Installation

1. Installation von Python von ([python.org](https://www.python.org/downloads/))

2. Unter Linux: Installation von Tkinter, falls nicht vorhanden:

```sh
sudo apt install python3-tk
```

## Starten

```sh
python start_prototype.py
```

## Hinweise

Das Programm ist darauf ausgelegt, dass mehrere Instanzen (auch auf verschiedenen Rechnern) gleichzeitig auf dieselbe Netzdatei zugreifen und diese verändern können.

Bereits vor dem Start des Programms sollte für jede Lerngruppe eine eigene Netzdatei erstellt und über die Netzwerkfunktion der Rechner (z. B. in einem Gruppenordner) für alle Mitglieder verfügbar sein. Eine Netzdatei ist einfach eine leere Datei mit der Endung `.net` (z.B. `mein_netz.net`). Beim Start des Programms kann die Datei von den Nutzer:innen ausgewählt werden. Wird keine Datei ausgewählt, wird automatisch eine neue Netzdatei unter der Standardadresse `data/wan.net` im Projektordner erstellt und verwendet.

Weitere Schreibrechte (für das Exportieren eigener Einstellungen/Programmzustände) werden nur an den Speicherorten benötigt, die von den Nutzer:innen gewählt werden.

## Projektstruktur

- `start_prototype.py` – Einstiegspunkt zum Starten der Anwendung
- `engine/` – enthält das GUI-Modul, das Logik-Modul und das Core-Modul:
    - `gui/` – grafische Benutzeroberfläche (Tkinter-basiert)
    - `logic/` – Steuerung der Abläufe, Verarbeitung der Benutzereingaben, zentrale Datenhaltung und Verwaltung des Binärstroms
    - `core.py` – Hauptinstanz des Programms

## Lizenz

Dieses Projekt ist eine Open Educational Resource (OER). Die Weiterentwicklung und nicht-kommerzielle Nutzung ist ausdrücklich erlaubt und erwünscht. Kommerzielle Nutzung (z.B. Verkauf, kostenpflichtige Angebote) ist nicht gestattet.