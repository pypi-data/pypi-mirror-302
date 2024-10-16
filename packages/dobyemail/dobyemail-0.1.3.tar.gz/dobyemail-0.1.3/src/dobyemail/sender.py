import smtplib
import imaplib
import logging
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .is_valid_email import is_valid_email

logger = logging.getLogger(__name__)

class Sender:
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
            raise ValueError("Missing required email sender configuration parameters")

    def send_email(self, to_email, subject, body, is_html=False, attachments=[]):
        if not is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return "Email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")
            return f"Failed to send email: {str(e)}"

    def send_email_with_attachments(self, to_email, subject, body, attachments):
        if not is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]

            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return "Email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")
            return f"Failed to send email: {str(e)}"

    def send_html_email(self, to_email, subject, html_body):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"HTML email sent successfully to {to_email}")
            return "HTML email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send HTML email to {to_email}. Error: {str(e)}")
            return f"Failed to send HTML email: {str(e)}"

    def send_bulk_email(self, to_emails, subject, body):
        successful_sends = 0
        failed_sends = 0

        for email in to_emails:
            result = self.send_email(email, subject, body)
            if "successfully" in result:
                successful_sends += 1
            else:
                failed_sends += 1

        return f"Bulk email sent. Successful: {successful_sends}, Failed: {failed_sends}"

    def save_to_draft(self, to_email, subject, body, is_html=False, attachments=[]):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap:
                imap.login(self.username, self.password)
                imap.select('"[Gmail]/Drafts"')
                imap.append('"[Gmail]/Drafts"', '', imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))
            logger.info(f"Email saved as draft")
            return "Email saved as draft successfully"
        except Exception as e:
            logger.error(f"Failed to save email as draft. Error: {str(e)}")
            return f"Failed to save email as draft: {str(e)}"

    def send_from_draft(self, draft_id):
        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap:
                imap.login(self.username, self.password)
                imap.select('"[Gmail]/Drafts"')
                _, msg_data = imap.fetch(draft_id, '(RFC822)')
                email_body = msg_data[0][1]
                
                # Send the email
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                    if self.smtp_use_tls:
                        smtp.starttls()
                    smtp.login(self.username, self.password)
                    smtp.sendmail(self.username, email_body['To'], email_body.as_string())
                
                # Delete the draft
                imap.store(draft_id, '+FLAGS', '\\Deleted')
                imap.expunge()
            
            logger.info(f"Email sent from draft successfully")
            return "Email sent from draft successfully"
        except Exception as e:
            logger.error(f"Failed to send email from draft. Error: {str(e)}")
            return f"Failed to send email from draft: {str(e)}"

def create_sender(smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password):
    """
    Factory method to create a Sender instance based on the provided parameters.
    """
    return Sender(smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password)
