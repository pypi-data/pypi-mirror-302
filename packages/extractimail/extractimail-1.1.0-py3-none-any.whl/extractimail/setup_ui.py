# setup_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from extractimail import config
import subprocess
import os
import sys

def run_setup():
    # Load existing config or defaults
    current_config = config.load_config()

    root = tk.Tk()
    root.title("Email Recollection Tool Configuration")

    # Outlook Folder Name
    tk.Label(root, text="Outlook Folder Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    folder_name_var = tk.StringVar(value=current_config.get("FOLDER_NAME", "Certificates_genAI_test"))
    tk.Entry(root, textvariable=folder_name_var, width=40).grid(row=0, column=1, padx=10, pady=5)

    # Save Path
    tk.Label(root, text="Save Path:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    save_path_var = tk.StringVar(value=current_config.get("SAVE_PATH", ""))
    tk.Entry(root, textvariable=save_path_var, width=40).grid(row=1, column=1, padx=10, pady=5)

    # Browse Button for Save Path
    def browse_save_path():
        path = filedialog.askdirectory()
        if path:
            save_path_var.set(path)

    tk.Button(root, text="Browse", command=browse_save_path).grid(row=1, column=2, padx=10, pady=5)

    # Days Back
    tk.Label(root, text="Days Back:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    days_back_var = tk.StringVar(value=str(current_config.get("DAYS_BACK", 6)))
    tk.Entry(root, textvariable=days_back_var, width=40).grid(row=2, column=1, padx=10, pady=5)

    # Schedule Day
    tk.Label(root, text="Schedule Day (MON, TUE, etc.):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    schedule_day_var = tk.StringVar(value=current_config.get("SCHEDULE_DAY", "THU"))
    tk.Entry(root, textvariable=schedule_day_var, width=40).grid(row=3, column=1, padx=10, pady=5)

    # Schedule Time
    tk.Label(root, text="Schedule Time (HH:MM, 24-hour):").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    schedule_time_var = tk.StringVar(value=current_config.get("SCHEDULE_TIME", "12:18"))
    tk.Entry(root, textvariable=schedule_time_var, width=40).grid(row=4, column=1, padx=10, pady=5)

    def save_settings():
        try:
            days = int(days_back_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Days Back must be an integer.")
            return

        schedule_day = schedule_day_var.get().upper()
        schedule_time = schedule_time_var.get()

        # Validate Schedule Day
        valid_days = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}
        if schedule_day not in valid_days:
            messagebox.showerror("Invalid Input", "Schedule Day must be one of MON, TUE, WED, THU, FRI, SAT, SUN.")
            return

        # Validate Schedule Time
        if not validate_time(schedule_time):
            messagebox.showerror("Invalid Input", "Schedule Time must be in HH:MM 24-hour format.")
            return

        config_data = {
            "FOLDER_NAME": folder_name_var.get(),
            "SAVE_PATH": save_path_var.get(),
            "DAYS_BACK": days,
            "SCHEDULE_DAY": schedule_day,
            "SCHEDULE_TIME": schedule_time
        }
        config.save_config(config_data)
        try:
            schedule_task(config_data)
            messagebox.showinfo("Success", "Configuration saved and scheduled task created successfully!")
            root.destroy()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create scheduled task: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def validate_time(time_str):
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour < 24 and 0 <= minute < 60
        except:
            return False

    def schedule_task(config_data):
        python_executable = sys.executable  # Dynamically get the Python executable path
        module_name = "extractimail"

        # Build the command to be run by the scheduled task
        command_to_run = f'"{python_executable}" -m {module_name}'

        # Create a batch file in a directory within the user's home directory
        batch_file_dir = os.path.join(os.path.expanduser("~"), "extractimail_scripts")
        os.makedirs(batch_file_dir, exist_ok=True)
        batch_file_path = os.path.join(batch_file_dir, "run_extractimail.bat")

        # Define the path for the log file
        log_file_path = os.path.join(batch_file_dir, "extractimail_output.log")

        with open(batch_file_path, 'w') as batch_file:
            batch_file.write(f'@echo off\n')
            batch_file.write(f'{command_to_run} >> "{log_file_path}" 2>&1\n')

        # Ensure the batch file has execute permissions (not typically an issue on Windows)
        os.chmod(batch_file_path, 0o755)

        # Build the schtasks command to schedule the batch file
        # Enclose the batch file path in quotes to handle any spaces
        schtasks_command = [
            'schtasks',
            '/Create',
            '/SC', 'WEEKLY',
            '/D', config_data["SCHEDULE_DAY"],
            '/TN', 'ExtractIMailTask',
            '/TR', f'"{batch_file_path}"',
            '/ST', config_data["SCHEDULE_TIME"],
            '/F'  # Forcefully create the task, overwriting if it exists
        ]

        # For debugging: print the command being run
        print(f"Running command: {schtasks_command}")

        # Run the schtasks command
        subprocess.run(schtasks_command, check=True)

    # Save Button
    tk.Button(root, text="Save Settings", command=save_settings).grid(row=5, column=1, pady=20)

    root.mainloop()