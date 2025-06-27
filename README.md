# SDCard Cleaner

**SDCard Cleaner** ist eine inhouse entwickelte Anwendung für die 3D-Druck-Workshops am Walter Reis Institut. Sie dient dazu, USB-Sticks und SD-Karten, die an 3D-Druckern verwendet werden, schnell und sicher von unerwünschten Dateien zu bereinigen – wichtige Dateien wie Druckmodelle und Firmware bleiben dabei erhalten.

---

## Was macht das Tool?

- **Automatische Erkennung von USB-Laufwerken/SD-Karten**
- **Löscht alle Dateien**, die nicht bestimmte Schlüsselwörter im Namen enthalten (z.B. `lucky_cat`, `firmware`, `CALIBRAT`)
- **Schützt wichtige Dateien** vor versehentlichem Löschen
- **CLI- und GUI-Variante** verfügbar

---

## Installation der Abhängigkeiten

Das Tool benötigt Python 3 (empfohlen: Python 3.8 oder neuer) und folgende Pakete:

- `pywin32` (für Windows-Laufwerkszugriff)
- `tkinter` (für die grafische Oberfläche, meist bei Windows-Python vorinstalliert)

Installieren Sie die Abhängigkeiten mit:

```bash
pip install pywin32
```

Falls `tkinter` nicht installiert ist, installieren Sie es unter Windows über die Python-Installation oder das Paketmanagement Ihrer Distribution (Linux: `sudo apt-get install python3-tk`).

---

## Verwendung

### 1. Kommandozeilen-Variante (CLI)

Starten Sie das Tool mit:

```bash
python cleansd.py
```

Das Programm überwacht angeschlossene USB-Laufwerke und fragt, ob ein gefundenes Laufwerk bereinigt werden soll. Es werden nur Dateien gelöscht, die **keines** der erlaubten Schlüsselwörter im Namen enthalten.

### 2. Grafische Benutzeroberfläche (GUI)

Starten Sie die GUI mit:

```bash
python cleansdgui.py
```

- Wählen Sie das gewünschte Laufwerk aus der Liste.
- Klicken Sie auf „Clean Selected Drive“, um die Bereinigung zu starten.
- Der Fortschritt und die gelöschten Dateien werden angezeigt.

---

## Erstellung einer ausführbaren Datei (EXE)

Um eine eigenständige `.exe`-Datei zu erstellen (z.B. für die Nutzung ohne Python-Installation), verwenden Sie [PyInstaller](https://pyinstaller.org/):

1. Installieren Sie PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Erstellen Sie die EXE für die CLI-Variante:
   ```bash
   pyinstaller --onefile cleansd.py
   ```
   Oder für die GUI-Variante:
   ```bash
   pyinstaller --onefile --windowed cleansdgui.py
   ```
3. Die ausführbare Datei finden Sie im `dist`-Ordner.

---

## Hinweise

- Das Tool ist **nur für Windows** geeignet (wegen `pywin32`).
- Es werden keine Systemlaufwerke oder Netzlaufwerke bereinigt.
- Die Anwendung ist speziell für die Anforderungen der 3D-Druck-Workshops am Walter Reis Institut entwickelt worden.

---

## Kontakt

Entwickelt von Tim Arnold für das Walter Reis Institut.
