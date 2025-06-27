
import os
import time
import win32file

# Allowed keywords in file names
ALLOWED_KEYWORDS = ["lucky_cat", "firmware", "CALIBRAT"]

# Function to detect connected drives
def get_connected_drives():
    drives = []
    drive_bits = win32file.GetLogicalDrives()
    for letter in range(26):
        if drive_bits & (1 << letter):
            drives.append(f"{chr(65 + letter)}:\\")
    return drives

# Function to check if a drive has a medium inserted
def is_drive_inserted(drive_path):
    return os.path.exists(drive_path) and os.path.isdir(drive_path)

# Function to clean up unwanted files from the USB drive
def clean_usb_drive(drive_path):
    try:
        # Check if the drive has a medium inserted
        if not is_drive_inserted(drive_path):
            #print(f"No medium inserted in drive {drive_path}. Skipping...")
            return

        # Check for files containing the name "lucky_cat"
        lucky_cat_found = False
        for item in os.listdir(drive_path):
            item_path = os.path.join(drive_path, item)

            # Ignore folders
            if os.path.isdir(item_path):
                continue

            # Check if the file contains "lucky_cat" in its name
            if "lucky_cat" in item:
                lucky_cat_found = True
                break

        # Warn the user if no file containing "lucky_cat" was found
        if not lucky_cat_found:
            print(f"Warning: No file containing 'lucky_cat' found on {drive_path}")

        # Proceed with cleaning the drive if confirmed
        confirm = input(f"Do you want to clean the drive {drive_path}? (y/N): ").strip().lower()
        if confirm != 'y':
            print(f"Skipping cleaning for drive {drive_path}")
            return

        # Delete files without allowed keywords in the name
        for item in os.listdir(drive_path):
            item_path = os.path.join(drive_path, item)

            # Ignore folders
            if os.path.isdir(item_path):
                continue

            # Delete files without allowed keywords in the name
            if not any(keyword in item for keyword in ALLOWED_KEYWORDS):
                print(f"Deleting: {item_path}")
                os.remove(item_path)
    except Exception as e:
        print(f"Error cleaning drive {drive_path}: {e}")

# Main function to monitor and process USB drives
def monitor_usb_drives():
    print("Monitoring for USB drives... Press Ctrl+C to stop.")
    known_drives = set(get_connected_drives())

    try:
        while True:
            time.sleep(1)
            current_drives = set(get_connected_drives())

            # Detect newly connected drives
            new_drives = current_drives - known_drives

            for drive in new_drives:
                print(f"New USB drive detected: {drive}")
                clean_usb_drive(drive)

            # Update known drives
            known_drives = current_drives

    except KeyboardInterrupt:
        print("Stopping USB monitoring.")

if __name__ == "__main__":
    monitor_usb_drives()
