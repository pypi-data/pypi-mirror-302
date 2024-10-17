import win32com.client
import os
from datetime import datetime, timedelta
import sys
import PyPDF2
import pandas as pd
import argparse
from extractimail import config
from extractimail import setup_ui

# Constants
ALLOWED_EXTENSIONS = ['.pdf', '.xlsx', '.csv']  # Allowed attachment types

def connect_to_outlook():
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        return outlook
    except Exception as e:
        print(f"Failed to connect to Outlook: {e}")
        sys.exit(1)

def access_target_folder(outlook, folder_name):
    try:
        inbox = outlook.GetDefaultFolder(6)
        target_folder = inbox.Folders[folder_name]
        return target_folder
    except Exception as e:
        print(f"Failed to access folder '{folder_name}': {e}")
        sys.exit(1)

def ensure_save_path(save_path):
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
        except Exception as e:
            print(f"Failed to create directory '{save_path}': {e}")
            sys.exit(1)

def filter_messages_by_date(target_folder, days):
    cutoff_date = datetime.now() - timedelta(days=days)
    formatted_cutoff = cutoff_date.strftime("%m/%d/%Y %H:%M %p")
    try:
        messages = target_folder.Items
        messages = messages.Restrict(f"[ReceivedTime] >= '{formatted_cutoff}'")
        return messages
    except Exception as e:
        print(f"Failed to retrieve emails: {e}")
        sys.exit(1)

def save_and_process_attachments(messages, save_path):
    for message in messages:
        try:
            if message.Class != 43:
                continue
            attachments = message.Attachments
            for i in range(1, attachments.Count + 1):
                attachment = attachments.Item(i)
                attachment_filename = attachment.FileName
                file_extension = os.path.splitext(attachment_filename)[1].lower()
                if file_extension not in ALLOWED_EXTENSIONS:
                    continue
                attachment_path = os.path.join(save_path, attachment_filename)
                # Handle duplicate filenames
                original_attachment_path = attachment_path
                counter = 1
                while os.path.exists(attachment_path):
                    name, extension = os.path.splitext(original_attachment_path)
                    attachment_path = f"{name}_{counter}{extension}"
                    counter += 1
                # Save the attachment
                attachment.SaveAsFile(attachment_path)
                # Process the attachment based on its type
                if file_extension == '.pdf':
                    extract_pdf_text(attachment_path)
                elif file_extension == '.xlsx':
                    extract_excel_data(attachment_path)
                elif file_extension == '.csv':
                    extract_csv_data(attachment_path)
        except Exception as e:
            print(f"Failed to process an email: {e}")
            continue

def extract_pdf_text(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            # Process the extracted text as needed
    except Exception as e:
        print(f"Failed to extract text from PDF '{file_path}': {e}")

def extract_excel_data(file_path):
    try:
        df = pd.read_excel(file_path)
        # Process the DataFrame as needed
    except Exception as e:
        print(f"Failed to read Excel file '{file_path}': {e}")

def extract_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Process the DataFrame as needed
    except Exception as e:
        print(f"Failed to read CSV file '{file_path}': {e}")

def run_setup_ui():
    setup_ui.run_setup()

def main():
    parser = argparse.ArgumentParser(description="Email Recollection Tool")
    parser.add_argument('--setup', action='store_true', help="Run configuration setup")
    args = parser.parse_args()

    # Automatically run setup if configuration is missing
    if not os.path.exists(config.CONFIG_FILE):
        print("Configuration file not found. Launching setup...")
        run_setup_ui()
        # Reload the config after setup
        cfg = config.load_config()
    else:
        cfg = config.load_config()

    if args.setup:
        run_setup_ui()
        sys.exit(0)

    # Initialize Outlook connection
    outlook = connect_to_outlook()

    # Ensure the save directory exists
    ensure_save_path(cfg["SAVE_PATH"])

    # Access the target Outlook folder
    target_folder = access_target_folder(outlook, cfg["FOLDER_NAME"])

    # Filter emails by the specified date range
    messages = filter_messages_by_date(target_folder, cfg["DAYS_BACK"])

    # Save and process attachments
    save_and_process_attachments(messages, cfg["SAVE_PATH"])

if __name__ == "__main__":
    main()