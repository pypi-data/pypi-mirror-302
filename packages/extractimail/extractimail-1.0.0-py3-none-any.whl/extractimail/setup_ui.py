# setup_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import config

def browse_save_path():
    path = filedialog.askdirectory()
    if path:
        save_path_var.set(path)

def save_settings():
    try:
        days = int(days_back_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Days Back must be an integer.")
        return

    config_data = {
        "FOLDER_NAME": folder_name_var.get(),
        "SAVE_PATH": save_path_var.get(),
        "DAYS_BACK": days,
        "ALLOWED_EXTENSIONS": [ext.strip() for ext in extensions_var.get().split(",")]
    }
    config.save_config(config_data)
    messagebox.showinfo("Success", "Configuration saved successfully!")
    root.destroy()

def run_setup():
    # Load existing config or defaults
    current_config = config.load_config()

    root = tk.Tk()
    root.title("Email Recollection Tool Configuration")

    # Folder Name
    tk.Label(root, text="Outlook Folder Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    folder_name_var = tk.StringVar(value=current_config["FOLDER_NAME"])
    tk.Entry(root, textvariable=folder_name_var, width=40).grid(row=0, column=1, padx=10, pady=5)

    # Save Path
    tk.Label(root, text="Save Path:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    save_path_var = tk.StringVar(value=current_config["SAVE_PATH"])
    tk.Entry(root, textvariable=save_path_var, width=40).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=browse_save_path).grid(row=1, column=2, padx=10, pady=5)

    # Days Back
    tk.Label(root, text="Days Back:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    days_back_var = tk.StringVar(value=str(current_config["DAYS_BACK"]))
    tk.Entry(root, textvariable=days_back_var, width=40).grid(row=2, column=1, padx=10, pady=5)

    # Allowed Extensions
    tk.Label(root, text="Allowed Extensions (comma-separated):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    extensions_var = tk.StringVar(value=",".join(current_config["ALLOWED_EXTENSIONS"]))
    tk.Entry(root, textvariable=extensions_var, width=40).grid(row=3, column=1, padx=10, pady=5)

    # Save Button
    tk.Button(root, text="Save Settings", command=save_settings).grid(row=4, column=1, pady=20)

    root.mainloop()
