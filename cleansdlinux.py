import os
import time
import getpass

# Erlaubte Schlüsselwörter in Dateinamen
ALLOWED_KEYWORDS = ["lucky_cat","Lucky_Cat","LuckyCat","firmware", "CALIBRAT"]

# Mount-Pfade (abhängig von Distribution & Desktop Environment ggf. anpassen)
MOUNT_PATHS = [
    f"/media/{getpass.getuser()}",
    f"/run/media/{getpass.getuser()}"
]

# Funktion zur Erkennung von eingehängten USB-Laufwerken
def get_connected_drives():
    drives = []
    for base_path in MOUNT_PATHS:
        if os.path.exists(base_path):
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.ismount(full_path):
                    drives.append(full_path)
    return drives

# Prüfen, ob ein Medium eingehängt ist (ein Mountpoint existiert)
def is_drive_inserted(drive_path):
    return os.path.ismount(drive_path)

# Funktion zur Säuberung eines USB-Laufwerks
def clean_usb_drive(drive_path):
    try:
        if not is_drive_inserted(drive_path):
            return

        lucky_cat_found = False
        for item in os.listdir(drive_path):
            item_path = os.path.join(drive_path, item)

            if os.path.isdir(item_path):
                continue

            if "lucky_cat" in item:
                lucky_cat_found = True
                break

        if not lucky_cat_found:
            print(f"Hinweis: Keine Datei mit 'lucky_cat' auf {drive_path} gefunden.")

        confirm = input(f"Möchtest du das Laufwerk {drive_path} bereinigen? (j/n): ").strip().lower()
        if confirm != 'j':
            print(f"Bereinigung für {drive_path} übersprungen.")
            return

        for item in os.listdir(drive_path):
            item_path = os.path.join(drive_path, item)

            if os.path.isdir(item_path):
                continue

            if not any(keyword in item for keyword in ALLOWED_KEYWORDS):
                print(f"Lösche: {item_path}")
                os.remove(item_path)

    except Exception as e:
        print(f"Fehler beim Bereinigen von {drive_path}: {e}")

# Hauptfunktion zum Überwachen von USB-Sticks
def monitor_usb_drives():
    print("Überwache USB-Laufwerke... (Strg+C zum Beenden)")
    known_drives = set(get_connected_drives())

    try:
        while True:
            time.sleep(1)
            current_drives = set(get_connected_drives())
            new_drives = current_drives - known_drives

            for drive in new_drives:
                print(f"Neues USB-Laufwerk erkannt: {drive}")
                clean_usb_drive(drive)

            known_drives = current_drives

    except KeyboardInterrupt:
        print("USB-Überwachung beendet.")

if __name__ == "__main__":
    monitor_usb_drives()
