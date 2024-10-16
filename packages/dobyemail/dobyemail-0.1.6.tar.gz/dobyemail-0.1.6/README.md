# [DobyEmail](python.dobyemail.com)

DobyEmail is a comprehensive Python package for handling various email operations. 
It provides a set of utilities and classes to simplify email-related tasks in your Python projects.

## Features

DobyEmail offers the following key functionalities:

1. **Email Service**: A high-level `Service` class that encapsulates SMTP and IMAP operations for sending and receiving emails.
2. **Email Sending**: The `Sender` class provides methods for composing and sending emails, including support for attachments.
3. **Email Reading**: The `Reader` class allows you to connect to an IMAP server, fetch emails, and parse their content.
4. **Email Transfer**: The `Transfer` class facilitates moving emails between different email accounts or folders.
5. **Date Parsing**: The `parse_date` function helps in converting various date string formats to a standardized format.
6. **Port Checking**: The `check_ports` function allows you to verify if specific ports are open on a given host.
7. **Email Validation**: The `is_valid_email` function provides basic validation for email addresses.
8. **Email Port Configuration**: The `get_email_ports` function retrieves standard email port configurations.

## Installation

```bash
pip install dobyemail
```

## Usage Examples

### Using the Service class

```python
from dobyemail import Service, config

service = Service(
    smtp_server=config.smtp_server,
    smtp_port=config.smtp_port,
    smtp_use_tls=config.smtp_use_tls,
    imap_server=config.imap_server,
    imap_port=config.imap_port,
    imap_use_ssl=config.imap_use_ssl,
    username=config.username,
    password=config.password
)

# Send an email
service.send_email("recipient@example.com", "Test Subject", "This is a test email.")

# Read emails
emails = service.read_emails(limit=5)
for email in emails:
    print(f"From: {email['from']}, Subject: {email['subject']}")
```

### Using the Sender class directly

```python
from dobyemail import Sender

sender = Sender(
    smtp_server="smtp.example.com",
    smtp_port=587,
    use_tls=True,
    username="your_username",
    password="your_password"
)

# Send a simple email
sender.send_email("recipient@example.com", "Hello", "This is a test email")

# Send an email with attachment
sender.send_email(
    "recipient@example.com",
    "Email with Attachment",
    "Please find the attached document.",
    attachments=["path/to/document.pdf"]
)
```

### Using the Reader class directly

```python
from dobyemail import Reader

reader = Reader(
    imap_server="imap.example.com",
    imap_port=993,
    use_ssl=True,
    username="your_username",
    password="your_password"
)

# Read the latest 10 emails
emails = reader.read_emails(limit=10)
for email in emails:
    print(f"Subject: {email['subject']}, From: {email['from']}")

# Search for emails with a specific subject
search_results = reader.search_emails("subject", "Important Meeting")
for email in search_results:
    print(f"Found email: {email['subject']}")
```

### Using the Transfer class

```python
from dobyemail import Transfer, Reader, Sender

source_reader = Reader(
    imap_server="source_imap.example.com",
    imap_port=993,
    use_ssl=True,
    username="source_username",
    password="source_password"
)

destination_sender = Sender(
    smtp_server="dest_smtp.example.com",
    smtp_port=587,
    use_tls=True,
    username="dest_username",
    password="dest_password"
)

transfer = Transfer(source_reader, destination_sender)

# Transfer the latest 5 emails
transferred_emails = transfer.transfer_emails(limit=5)
print(f"Transferred {len(transferred_emails)} emails")
```

### Utility Functions

```python
from dobyemail import parse_date, check_ports, is_valid_email, get_email_ports

# Parse a date string
print(parse_date("2023-05-15"))  # Output: "15-May-2023"

# Check if ports are open
print(check_ports("example.com", [80, 443]))

# Validate an email address
print(is_valid_email("user@example.com"))  # Output: True

# Get standard email ports
print(get_email_ports())
```

## Running Tests

To run the unit tests, use the following command from the project root directory:

```bash
python -m unittest discover tests
```

## Configuration

The `email_ports.json` file is used for configuring email ports. It is loaded automatically by the `Config` class in `config.py`. You can modify this file to add or update email port configurations.

## Contributing

Please read CONTRIBUTE.md for details on our code of conduct, and the process for submitting pull requests and publishing to PyPI.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
