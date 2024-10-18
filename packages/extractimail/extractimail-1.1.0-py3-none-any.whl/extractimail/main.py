# main.py
import win32com.client
import os
from datetime import datetime, timedelta
import sys
import PyPDF2
import pandas as pd
import argparse
import subprocess
from extractimail import config
from extractimail import setup_ui
import logging
import pytz  # Ensure pytz is installed: pip install pytz

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.expanduser('~'), 'extractimail.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants
ALLOWED_EXTENSIONS = ['.pdf', '.xlsx', '.csv']  # Supported attachment types

def connect_to_outlook():
    logging.debug("Attempting to connect to Outlook.")
    print("Connecting to Outlook...")
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        logging.info("Connected to Outlook successfully.")
        print("Connected to Outlook successfully.")
        return outlook
    except Exception as e:
        logging.error(f"Failed to connect to Outlook: {e}")
        print(f"Failed to connect to Outlook: {e}")
        sys.exit(1)

def access_target_folder(outlook, folder_name):
    logging.debug(f"Accessing Outlook folder: {folder_name}")
    print(f"Accessing Outlook folder: {folder_name}")
    try:
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
        # Log all subfolders for verification
        logging.debug("Listing all subfolders in Inbox:")
        for folder in inbox.Folders:
            logging.debug(f"Found folder: {folder.Name}")
        target_folder = inbox.Folders[folder_name]
        logging.info(f"Accessed folder '{folder_name}' successfully.")
        print(f"Accessed folder '{folder_name}' successfully.")
        return target_folder
    except Exception as e:
        logging.error(f"Failed to access folder '{folder_name}': {e}")
        print(f"Failed to access folder '{folder_name}': {e}")
        sys.exit(1)

def ensure_save_path(save_path):
    logging.debug(f"Ensuring save path exists: {save_path}")
    print(f"Ensuring save path exists: {save_path}")
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
            logging.info(f"Created directory '{save_path}'.")
            print(f"Created directory '{save_path}'.")
        except Exception as e:
            logging.error(f"Failed to create directory '{save_path}': {e}")
            print(f"Failed to create directory '{save_path}': {e}")
            sys.exit(1)
    else:
        logging.debug(f"Save path '{save_path}' already exists.")
        print(f"Save path '{save_path}' already exists.")

def filter_messages_by_date(target_folder, days):
    # Define the timezone; replace 'Your/Timezone' with your actual timezone, e.g., 'Europe/Paris'
    timezone = pytz.timezone("Europe/Paris")  # Example: "Europe/Paris"
    now = datetime.now(timezone)
    cutoff_date = now - timedelta(days=days)
    logging.debug(f"Current time (timezone aware): {now}")
    print(f"Current time: {now}")
    logging.debug(f"Cutoff date (before formatting): {cutoff_date}")
    print(f"Cutoff date (before formatting): {cutoff_date}")
    formatted_cutoff = cutoff_date.strftime("%B %d, %Y %I:%M %p")  # Full month name
    logging.debug(f"Formatted cutoff_date: {formatted_cutoff}")
    print(f"Filtering messages received after {formatted_cutoff}.")
    try:
        messages = target_folder.Items
        total_messages = messages.Count
        logging.debug(f"Total messages in folder: {total_messages}")
        print(f"Total messages in folder: {total_messages}")
        messages = messages.Restrict(f"[ReceivedTime] >= '{formatted_cutoff}'")
        filtered_count = messages.Count
        logging.info(f"Retrieved {filtered_count} messages received after {formatted_cutoff}.")
        print(f"Retrieved {filtered_count} messages received after {formatted_cutoff}.")
        return messages
    except Exception as e:
        logging.error(f"Failed to retrieve emails: {e}")
        print(f"Failed to retrieve emails: {e}")
        sys.exit(1)

def save_and_process_attachments(messages, save_path):
    logging.debug("Starting to save and process attachments.")
    print("Starting to save and process attachments.")
    saved_attachments = 0

    for message in messages:
        try:
            if message.Class != 43:  # 43 refers to Mail Item
                continue

            attachments = message.Attachments
            attachment_count = attachments.Count

            if attachment_count > 0:
                logging.debug(f"Processing email: {message.Subject} with {attachment_count} attachments.")
                print(f"Processing email: {message.Subject} with {attachment_count} attachments.")

                for i in range(1, attachment_count + 1):
                    attachment = attachments.Item(i)
                    attachment_filename = attachment.FileName
                    file_extension = os.path.splitext(attachment_filename)[1].lower()

                    if file_extension not in ALLOWED_EXTENSIONS:
                        logging.debug(f"Skipping unsupported file type: {attachment_filename}")
                        print(f"Skipping unsupported file type: {attachment_filename}")
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
                    saved_attachments += 1
                    logging.info(f"Saved attachment: {attachment_path}")
                    print(f"Saved attachment: {attachment_path}")

                    # Process the attachment based on its type
                    if file_extension == '.pdf':
                        extract_pdf_text(attachment_path)
                    elif file_extension == '.xlsx':
                        extract_excel_data(attachment_path)
                    elif file_extension == '.csv':
                        extract_csv_data(attachment_path)

        except Exception as e:
            logging.error(f"Failed to process an email: {e}")
            print(f"Failed to process an email: {e}")
            continue

    logging.info(f"Total attachments saved: {saved_attachments}")
    print(f"Total attachments saved: {saved_attachments}")

def extract_pdf_text(file_path):
    logging.debug(f"Extracting text from PDF: {file_path}")
    print(f"Extracting text from PDF: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            logging.info(f"Extracted text from PDF '{file_path}'.")
            print(f"Extracted text from PDF '{file_path}'.")
            # Implement further processing if needed
    except Exception as e:
        logging.error(f"Failed to extract text from PDF '{file_path}': {e}")
        print(f"Failed to extract text from PDF '{file_path}': {e}")

def extract_excel_data(file_path):
    logging.debug(f"Extracting data from Excel file: {file_path}")
    print(f"Extracting data from Excel file: {file_path}")
    try:
        df = pd.read_excel(file_path)
        logging.info(f"Extracted data from Excel '{file_path}'.")
        print(f"Extracted data from Excel '{file_path}'.")
        # Implement further processing if needed
    except Exception as e:
        logging.error(f"Failed to read Excel file '{file_path}': {e}")
        print(f"Failed to read Excel file '{file_path}': {e}")

def extract_csv_data(file_path):
    logging.debug(f"Extracting data from CSV file: {file_path}")
    print(f"Extracting data from CSV file: {file_path}")
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Extracted data from CSV '{file_path}'.")
        print(f"Extracted data from CSV '{file_path}'.")
        # Implement further processing if needed
    except Exception as e:
        logging.error(f"Failed to read CSV file '{file_path}': {e}")
        print(f"Failed to read CSV file '{file_path}': {e}")

def run_setup_ui():
    logging.debug("Launching setup UI.")
    print("Launching setup UI.")
    setup_ui.run_setup()

def process_emails():
    # Load configuration
    cfg = config.load_config()
    logging.debug(f"Configuration loaded: {cfg}")
    print("Configuration loaded successfully.")

    # Initialize Outlook connection
    outlook = connect_to_outlook()

    # Ensure the save directory exists
    ensure_save_path(cfg["SAVE_PATH"])
    print(f"Save path set to: {cfg['SAVE_PATH']}")

    # Access the target Outlook folder
    target_folder = access_target_folder(outlook, cfg["FOLDER_NAME"])

    # Filter emails by the specified date range
    messages = filter_messages_by_date(target_folder, cfg["DAYS_BACK"])

    # Save and process attachments
    save_and_process_attachments(messages, cfg["SAVE_PATH"])

def main():
    parser = argparse.ArgumentParser(description="Email Recollection Tool")
    parser.add_argument('--setup', action='store_true', help="Run configuration setup")
    args = parser.parse_args()

    if args.setup:
        logging.info("Running setup via --setup argument.")
        print("Running setup via --setup argument.")
        run_setup_ui()
        sys.exit(0)

    # Check if configuration file exists
    if not os.path.exists(config.CONFIG_FILE):
        logging.error("Configuration file not found. Please run the setup using '--setup' argument.")
        print("Configuration file not found. Please run the setup using '--setup' argument.")
        sys.exit(1)
    else:
        cfg = config.load_config()
        logging.debug(f"Configuration loaded: {cfg}")

    logging.info("Starting email extraction and attachment processing.")
    print("Starting email extraction and attachment processing.")
    process_emails()
    logging.info("Email extraction and attachment processing completed successfully.")
    print("Email extraction and attachment processing completed successfully.")

if __name__ == "__main__":
    main()

# Expose process_emails for programmatic use
def run_without_args():
    try:
        process_emails()
    except Exception as e:
        logging.error(f"An error occurred during email processing: {e}")
        print(f"An error occurred during email processing: {e}")