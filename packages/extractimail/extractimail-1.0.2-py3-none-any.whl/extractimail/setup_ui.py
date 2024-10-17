# setup_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from extractimail import config
import subprocess
import os

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

    # Browse Button
    def browse_save_path():
        path = filedialog.askdirectory()
        if path:
            save_path_var.set(path)

    tk.Button(root, text="Browse", command=browse_save_path).grid(row=1, column=2, padx=10, pady=5)

    # Days Back
    tk.Label(root, text="Days Back:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    days_back_var = tk.StringVar(value=str(current_config["DAYS_BACK"]))
    tk.Entry(root, textvariable=days_back_var, width=40).grid(row=2, column=1, padx=10, pady=5)

    # Schedule Day
    tk.Label(root, text="Schedule Day (e.g., MON, TUE):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    schedule_day_var = tk.StringVar(value=current_config.get("SCHEDULE_DAY", "FRI"))
    tk.Entry(root, textvariable=schedule_day_var, width=40).grid(row=3, column=1, padx=10, pady=5)

    # Schedule Time
    tk.Label(root, text="Schedule Time (HH:MM):").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    schedule_time_var = tk.StringVar(value=current_config.get("SCHEDULE_TIME", "11:00"))
    tk.Entry(root, textvariable=schedule_time_var, width=40).grid(row=4, column=1, padx=10, pady=5)

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
            "SCHEDULE_DAY": schedule_day_var.get().upper(),
            "SCHEDULE_TIME": schedule_time_var.get()
        }
        config.save_config(config_data)
        schedule_task(config_data)
        messagebox.showinfo("Success", "Configuration saved successfully!")
        root.destroy()

    def schedule_task(config_data):
        executable_path = os.path.abspath("extractimail.exe")  # Adjust path if necessary
        schedule_day = config_data["SCHEDULE_DAY"]
        schedule_time = config_data["SCHEDULE_TIME"]

        command = [
            'schtasks',
            '/Create',
            '/SC', 'WEEKLY',
            '/D', schedule_day,
            '/TN', 'ExtractIMailTask',
            '/TR', f'"{executable_path}"',
            '/ST', schedule_time,
            '/F'
        ]
        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "Scheduled task created successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to schedule task: {e}")

    # Save Button
    tk.Button(root, text="Save Settings", command=save_settings).grid(row=5, column=1, pady=20)

    root.mainloop()