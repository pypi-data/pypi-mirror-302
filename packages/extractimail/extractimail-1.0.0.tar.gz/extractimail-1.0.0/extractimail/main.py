import win32com.client
import os
from datetime import datetime, timedelta
import sys
import PyPDF2
import pandas as pd
import argparse
import config
import setup_ui

# Configuration Constants are now loaded from config.py

def connect_to_outlook():
    """
    Connects to the Outlook application and returns the MAPI namespace.

    :return: Outlook MAPI namespace object
    """
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        print("Connected to Outlook successfully.")
        return outlook
    except Exception as e:
        print(f"Failed to connect to Outlook: {e}")
        sys.exit(1)

def access_target_folder(outlook, folder_name):
    """
    Accesses the specified Outlook folder.

    :param outlook: Outlook MAPI namespace object
    :param folder_name: Name of the Outlook folder to access
    :return: Target folder object
    """
    try:
        inbox = outlook.GetDefaultFolder(6)  # 6 corresponds to the Inbox
        print("Accessed the Inbox folder.")
        target_folder = inbox.Folders[folder_name]
        print(f"Accessed the folder: {folder_name}")
        return target_folder
    except Exception as e:
        print(f"Failed to access folder '{folder_name}': {e}")
        sys.exit(1)

def ensure_save_path(save_path):
    """
    Ensures that the save directory exists; creates it if it does not.

    :param save_path: Directory path to save attachments
    """
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
            print(f"Created directory: {save_path}")
        except Exception as e:
            print(f"Failed to create directory '{save_path}': {e}")
            sys.exit(1)

def filter_messages_by_date(target_folder, days):
    """
    Retrieves emails received within the specified number of days.

    :param target_folder: Target Outlook folder object
    :param days: Number of days to look back for emails
    :return: Filtered list of email messages
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    formatted_cutoff = cutoff_date.strftime("%m/%d/%Y %H:%M %p")
    try:
        messages = target_folder.Items
        messages = messages.Restrict(f"[ReceivedTime] >= '{formatted_cutoff}'")
        print(f"Retrieved emails received in the last {days} days.")
        return messages
    except Exception as e:
        print(f"Failed to retrieve emails: {e}")
        sys.exit(1)

def save_and_process_attachments(messages, save_path, allowed_extensions):
    """
    Saves and processes PDF and XLSX attachments from the filtered emails.

    :param messages: List of filtered email messages
    :param save_path: Directory path to save attachments
    :param allowed_extensions: List of allowed file extensions
    """
    saved_attachments = 0

    for message in messages:
        try:
            # Ensure the item is a MailItem
            if message.Class != 43:  # 43 corresponds to MailItem
                continue

            attachments = message.Attachments
            attachment_count = attachments.Count

            if attachment_count > 0:
                print(f"\nEmail Subject: {message.Subject}")
                print(f"Number of attachments: {attachment_count}")

                for i in range(1, attachment_count + 1):
                    attachment = attachments.Item(i)
                    attachment_filename = attachment.FileName
                    file_extension = os.path.splitext(attachment_filename)[1].lower()

                    # Process only allowed file types
                    if file_extension not in allowed_extensions:
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
                    print(f"Saved attachment: {attachment_path}")
                    saved_attachments += 1

                    # Process the attachment based on its type
                    if file_extension == '.pdf':
                        extract_pdf_text(attachment_path)
                    elif file_extension == '.xlsx':
                        extract_excel_data(attachment_path)

        except Exception as e:
            print(f"Failed to process an email: {e}")
            continue

    print(f"\nTotal attachments saved: {saved_attachments}")

def extract_pdf_text(file_path):
    """
    Extracts and prints text from a PDF file.

    :param file_path: Path to the PDF file
    """
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            print(f"Extracted PDF Text from {os.path.basename(file_path)}:")
            print(text)
    except Exception as e:
        print(f"Failed to extract text from PDF '{file_path}': {e}")

def extract_excel_data(file_path):
    """
    Reads and prints data from an Excel file.

    :param file_path: Path to the Excel file
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Extracted Excel Data from {os.path.basename(file_path)}:")
        print(df)
    except Exception as e:
        print(f"Failed to read Excel file '{file_path}': {e}")

def run_setup_ui():
    """
    Runs the configuration setup UI.
    """
    setup_ui.run_setup()

def main():
    """
    Main function to execute the attachment saving and processing workflow.
    """
    parser = argparse.ArgumentParser(description="Email Recollection Tool")
    parser.add_argument('--setup', action='store_true', help="Run configuration setup")
    args = parser.parse_args()

    if args.setup:
        run_setup_ui()
        sys.exit(0)

    # Load configuration
    cfg = config.load_config()

    # Initialize Outlook connection
    outlook = connect_to_outlook()

    # Ensure the save directory exists
    ensure_save_path(cfg["SAVE_PATH"])

    # Access the target Outlook folder
    target_folder = access_target_folder(outlook, cfg["FOLDER_NAME"])

    # Filter emails by the specified date range
    messages = filter_messages_by_date(target_folder, cfg["DAYS_BACK"])

    # Save and process attachments
    save_and_process_attachments(messages, cfg["SAVE_PATH"], cfg["ALLOWED_EXTENSIONS"])

if __name__ == "__main__":
    main()