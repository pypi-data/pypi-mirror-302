from .sender import create_sender
from .reader import create_reader
from .transfer import create_transfer
from .check_ports import check_ports
from .config import config

class Service:
    def __init__(self, smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_use_tls = smtp_use_tls
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.imap_use_ssl = imap_use_ssl
        self.username = username
        self.password = password

        if not all([self.smtp_server, self.smtp_port, self.imap_server, self.imap_port, self.username, self.password]):
            raise ValueError("Missing required email configuration parameters")

        self.sender = create_sender(smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password)
        self.reader = create_reader(imap_server, imap_port, imap_use_ssl, username, password)
        self.transfer = create_transfer(imap_server, imap_port, imap_use_ssl, username, password)

    def test(self):
        # Extract ports from the email_ports dictionary
        email_ports_no = list(map(int, config.email_ports.keys()))

        # Use the SMTP server address for testing
        host_to_check = self.smtp_server

        # Check the ports and get results
        port_results = check_ports(host_to_check, email_ports_no)

        # Prepare result string
        result = ""
        for port in email_ports_no:
            protocol_info = config.email_ports[str(port)]
            status = port_results.get(port, "Unknown")
            result += f"{protocol_info['protocol']} {protocol_info['security']} Port {port}: {status}\n"

        return result

    def send_email(self, to_email, subject, body):
        return self.sender.send_email(to_email, subject, body)

    def list_emails(self, from_date, to_date):
        return self.reader.list_emails(from_date, to_date)

    def save_to_draft(self, to_email, subject, body, is_html=False, attachments=[]):
        return self.sender.save_to_draft(to_email, subject, body, is_html, attachments)

    def send_from_draft(self, draft_id):
        return self.sender.send_from_draft(draft_id)

    def remove_files_with_filters(self, download_folder, subject_filter=None, content_filter=None,
                                  from_date=None, to_date=None):
        return self.transfer.remove_files_with_filters(download_folder, subject_filter, content_filter,
                                                       from_date, to_date)

    def copy_messages(self, source_folder, destination_folder, criteria=None):
        return self.transfer.copy_messages(source_folder, destination_folder, criteria)

    def move_messages(self, source_folder, destination_folder, criteria=None):
        return self.transfer.move_messages(source_folder, destination_folder, criteria)

# Example of how to use the email service:
# 
# def create_service_example(config):
#     return Service(
#         smtp_server=config['smtp_server'],
#         smtp_port=config['smtp_port'],
#         smtp_use_tls=config['smtp_use_tls'],
#         imap_server=config['imap_server'],
#         imap_port=config['imap_port'],
#         imap_use_ssl=config['imap_use_ssl'],
#         username=config['username'],
#         password=config['password']
#     )
# 
# service = create_service_example(config)
# service.send_email(to_email, subject, body)
# service.list_emails(from_date, to_date)
# service.save_to_draft(to_email, subject, body)
# service.send_from_draft(draft_id)
# service.copy_messages('INBOX', 'Archive', 'SUBJECT "Important"')
# service.move_messages('INBOX', 'Trash', 'BEFORE "01-Jan-2022"')
