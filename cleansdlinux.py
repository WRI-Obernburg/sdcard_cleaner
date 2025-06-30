import os
import time
import getpass

# Allowed keywords in file names
ALLOWED_KEYWORDS = ["lucky_cat","Lucky_Cat","LuckyCat","firmware", "CALIBRAT"]

# Mount
MOUNT_PATHS = [
    f"/media/{getpass.getuser()}",
    f"/run/media/{getpass.getuser()}"
]

# Function to detect connected drives
def get_connected_drives():
    drives = []
    for base_path in MOUNT_PATHS:
        if os.path.exists(base_path):
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.ismount(full_path):
                    drives.append(full_path)
    return drives

#Function to check if a drive has a medium inserted
def is_drive_inserted(drive_path):
    return os.path.ismount(drive_path)

# Function to clean up unwanted files from the USB drive
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
            print(f"No file with 'lucky_cat' found on {drive_path} .")

        confirm = input(f"do you want to clean {drive_path} ? (j/n): ").strip().lower()
        if confirm != 'j':
            print(f"skipping cleaning for {drive_path} ")
            return

        for item in os.listdir(drive_path):
            item_path = os.path.join(drive_path, item)

            if os.path.isdir(item_path):
                continue

            if not any(keyword in item for keyword in ALLOWED_KEYWORDS):
                print(f"deleting: {item_path}")
                os.remove(item_path)

    except Exception as e:
        print(f"error while cleaning {drive_path}: {e}")

# Main function to monitor and process USB drives
def monitor_usb_drives():
    print("monitoring drives... (Strg+C to end programm)")
    known_drives = set(get_connected_drives())

    try:
        while True:
            time.sleep(1)
            current_drives = set(get_connected_drives())
            new_drives = current_drives - known_drives

            for drive in new_drives:
                print(f"new drive found: {drive}")
                clean_usb_drive(drive)

            known_drives = current_drives

    except KeyboardInterrupt:
        print(" stoped monitoring.")

if __name__ == "__main__":
    monitor_usb_drives()
