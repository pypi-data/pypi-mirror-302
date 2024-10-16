import os
import email
import imaplib
from .parse_date import parse_date

class Transfer:
    def __init__(self, imap_server, imap_port, imap_use_ssl, username, password):
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.imap_use_ssl = imap_use_ssl
        self.username = username
        self.password = password

    def remove_files_with_filters(self, download_folder, subject_filter=None, content_filter=None,
                                  from_date=None, to_date=None):
        """Removes email files based on the provided filters.

        Args:
            download_folder: The folder containing downloaded email files.
            subject_filter: A string to search for in the email subject.
            content_filter: A string to search for in the email content.
            from_date: The start date for filtering emails (inclusive).
            to_date: The end date for filtering emails (inclusive).
        """
        for filename in os.listdir(download_folder):
            filepath = os.path.join(download_folder, filename)
            if not os.path.isfile(filepath):
                continue

            with open(filepath, "r") as f:
                msg = email.message_from_file(f)

            subject = msg["Subject"]
            content = msg.get_payload(decode=True).decode()
            date_sent = parse_date(msg["Date"])

            if subject_filter and subject_filter not in subject:
                continue
            if content_filter and content_filter not in content:
                continue
            if from_date and date_sent < from_date:
                continue
            if to_date and date_sent > to_date:
                continue

            os.remove(filepath)
            print(f"Removed: {filename}")

    def copy_messages(self, source_folder, destination_folder, criteria=None):
        """
        Copy messages from one folder to another based on given criteria.
        
        Args:
            source_folder: The folder to copy messages from.
            destination_folder: The folder to copy messages to.
            criteria: IMAP search criteria to filter messages (e.g., 'SUBJECT "Important"').
        """
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap:
            imap.login(self.username, self.password)
            imap.select(source_folder)

            _, message_numbers = imap.search(None, criteria if criteria else 'ALL')
            for num in message_numbers[0].split():
                imap.copy(num, destination_folder)

            print(f"Copied {len(message_numbers[0].split())} messages from {source_folder} to {destination_folder}")

    def move_messages(self, source_folder, destination_folder, criteria=None):
        """
        Move messages from one folder to another based on given criteria.
        
        Args:
            source_folder: The folder to move messages from.
            destination_folder: The folder to move messages to.
            criteria: IMAP search criteria to filter messages (e.g., 'SUBJECT "Important"').
        """
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap:
            imap.login(self.username, self.password)
            imap.select(source_folder)

            _, message_numbers = imap.search(None, criteria if criteria else 'ALL')
            for num in message_numbers[0].split():
                imap.copy(num, destination_folder)
                imap.store(num, '+FLAGS', '\\Deleted')
            
            imap.expunge()

            print(f"Moved {len(message_numbers[0].split())} messages from {source_folder} to {destination_folder}")

def create_transfer(imap_server, imap_port, imap_use_ssl, username, password):
    """
    Factory method to create a Transfer instance based on the provided parameters.
    """
    return Transfer(imap_server, imap_port, imap_use_ssl, username, password)
