import os
import time
import win32file
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, ttk

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

# Function to check if a drive is a network drive
def is_network_device(drive_path):
    try:
        drive_type = win32file.GetDriveType(drive_path)
        return drive_type == win32file.DRIVE_REMOTE
    except Exception as e:
        print(f"Error checking network device status for {drive_path}: {e}")
        return False

# Function to clean up unwanted files from the USB drive
def clean_usb_drive(drive_path):
    try:
        if not is_drive_inserted(drive_path):
            messagebox.showwarning("No Medium", f"No medium inserted in drive {drive_path}. Skipping...")
            return
        if is_network_device(drive_path):
            messagebox.showwarning("Network Drive", f"Network drive {drive_path} detected. Skipping...")
            return
        if drive_path.startswith("C:\\"):
            messagebox.showwarning("Hard Drive", f"Hard drive {drive_path} detected. Skipping...")
            return
        drive_size = os.path.getsize(drive_path)
        if drive_size > 32 * 1024 * 1024 * 1024:
            messagebox.showwarning("Large Drive", f"Large drive {drive_path} detected. Skipping...")
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
            messagebox.showwarning("Warning", f"No file containing 'lucky_cat' found on {drive_path}")

        confirm = messagebox.askyesno("Confirm", f"Do you want to clean the drive {drive_path}?")
        if not confirm:
            return

        progress_bar['value'] = 0
        progress_text.set("0%")
        root.update_idletasks()

        files = [item for item in os.listdir(drive_path) if not os.path.isdir(os.path.join(drive_path, item))]
        progress_step = 100 / len(files) if files else 100

        start_time = time.time()

        deleted_files = []  # List to keep track of deleted files

        for index, item in enumerate(files):
            item_path = os.path.join(drive_path, item)
            if not any(keyword in item for keyword in ALLOWED_KEYWORDS):
                os.remove(item_path)
                deleted_files.append(item_path)  # Add deleted file to the list
                print(f"Deleted: {item_path}")
            progress_bar['value'] += progress_step
            progress_text.set(f"{int(progress_bar['value'])}%")
            root.update_idletasks()
            time.sleep(0.03)

        progress_bar['value'] = 100
        progress_text.set("100%")
        root.update_idletasks()

        # Display the deletion summary
        if deleted_files:
            deleted_files_str = "\n".join(deleted_files)
            messagebox.showinfo("Success", f"Cleaning completed for drive {drive_path}.\n\nDeleted files:\n{deleted_files_str}")
        else:
            messagebox.showinfo("Success", f"Cleaning completed for drive {drive_path}. No unwanted files found.")

    except Exception as e:
        messagebox.showerror("Error", f"Error cleaning drive {drive_path}: {e}")

# Update drive list and ensure the first entry is selected if no selection exists
def auto_update_drive_list():
    drives = get_connected_drives()
    drive_list.delete(0, tk.END)
    
    for drive in drives:
        if not is_drive_inserted(drive):
            continue
        if is_network_device(drive):
            continue
        if drive.startswith("C:\\"):
            continue
        drive_list.insert(tk.END, drive)

    # If no drive is selected, select the first item
    if not drive_list.curselection():
        drive_list.selection_set(0)

    root.after(1000, auto_update_drive_list)

# Info message box
def show_info():
    info_message = ("USB Drive Cleaner by Tim Arnold\n\n" "This software detects and cleans unwanted files from USB drives. "
                    "It skips hard drives, network drives, and large drives (>32GB). "
                    "The cleaning process removes all files except those containing the allowed keywords: "
                    f"{', '.join(ALLOWED_KEYWORDS)}.\n\n" "Select a drive from the list and click 'Clean Selected Drive' to start the process.")
    messagebox.showinfo("About", info_message)

root = tk.Tk()
root.title("USB Drive Cleaner")
root.geometry("450x400")
root.config(bg="#F0F0F0")

# Apply custom font and color to the window
font_style = ('Helvetica', 12)
highlight_color = "#4CAF50"

frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=10)

# disable resizing
root.resizable(False, False)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

drive_list = Listbox(frame, yscrollcommand=scrollbar.set, width=50, height=10, font=font_style, bg="#FFFFFF", selectbackground=highlight_color)
drive_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)
scrollbar.config(command=drive_list.yview)

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

progress_text = tk.StringVar(value="0%")
progress_label = tk.Label(root, textvariable=progress_text, font=font_style, bg="#F0F0F0", fg=highlight_color)
progress_label.pack(pady=2)

# Clean button
clean_button = tk.Button(root, text="Clean Selected Drive", command=lambda: clean_usb_drive(drive_list.get(tk.ACTIVE)),
                         font=font_style, bg=highlight_color, fg="white", relief="flat", padx=10, pady=5)
clean_button.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Info", command=lambda: show_info(), font=font_style, bg="blue", fg="white", relief="flat", padx=10, pady=5)
exit_button.pack(pady=10)

# Update drive list every second
auto_update_drive_list()
root.mainloop()
