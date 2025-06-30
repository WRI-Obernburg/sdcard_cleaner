import subprocess
import os
import time
import getpass

ALLOWED_KEYWORDS = ["lucky_cat", "Lucky_Cat", "LuckyCat", "firmware", "CALIBRAT"]

# Get all mounted and unmounted USB devices (vfat and FAT16 common for sticks)
def get_usb_devices():
    result = subprocess.run(["lsblk", "-o", "NAME,FSTYPE,LABEL,MOUNTPOINT,RM", "-J"],
                            capture_output=True, text=True)
    devices = []
    if result.returncode == 0:
        import json
        data = json.loads(result.stdout)
        for device in data["blockdevices"]:
            if not device.get("rm", False):
                continue  # only removable devices
            if device.get("children"):
                for part in device["children"]:
                    fstype = part.get("fstype", "")
                    if fstype.lower() in ["vfat", "fat16", "fat32"]:
                        name = part["name"]
                        mountpoint = part["mountpoint"]
                        devices.append({
                            "name": name,
                            "mountpoint": mountpoint,
                            "dev": f"/dev/{name}"
                        })
    return devices


# Try to mount if not already mounted
def ensure_mounted(device):
    if device["mountpoint"]:
        return device["mountpoint"]
    try:
        result = subprocess.run(["udisksctl", "mount", "-b", device["dev"]],
                                capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Mounted" in line and "at" in line:
                    return line.split(" at ")[-1].strip().rstrip(".")
    except Exception as e:
        print(f"Error mounting {device['dev']}: {e}")
    return None

# Check and clean USB drive contents
def clean_usb_drive(path):
    if not os.path.isdir(path):
        print(f"{path} is not accessible.")
        return

    lucky_cat_found = any("lucky_cat" in f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))
    if not lucky_cat_found:
        print(f"No 'lucky_cat' files found in {path}.")

    confirm = input(f"Do you want to clean {path}? (j/n): ").strip().lower()
    if confirm != "j":
        print("Skipping.")
        return

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            continue
        if not any(keyword in item for keyword in ALLOWED_KEYWORDS):
            try:
                print(f"Deleting {item_path}")
                os.remove(item_path)
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")

def monitor_usb():
    print("Monitoring USB devices... (Strg+C to stop)")
    seen = set()
    try:
        while True:
            time.sleep(1)
            devices = get_usb_devices()
            for dev in devices:
                if dev["dev"] in seen:
                    continue
                mountpoint = ensure_mounted(dev)
                if mountpoint:
                    print(f"New device mounted at: {mountpoint}")
                    clean_usb_drive(mountpoint)
                    seen.add(dev["dev"])
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    monitor_usb()
