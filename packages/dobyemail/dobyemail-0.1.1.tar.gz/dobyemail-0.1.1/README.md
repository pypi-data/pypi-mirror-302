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

## Project Structure

```
python.dobyemail.com/
├── src/
│   └── dobyemail/
│       ├── __init__.py
│       ├── config.py
│       ├── email_ports.json
│       ├── service.py
│       ├── sender.py
│       ├── reader.py
│       ├── transfer.py
│       ├── parse_date.py
│       ├── check_ports.py
│       ├── is_valid_email.py
│       └── get_email_ports.py
├── tests/
│   └── test_email_utils.py
├── README.md
├── requirements.txt
└── setup.py
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dobyemail/python.git
   ```

2. Change to the project directory:
   ```bash
   cd dobyemail
   ```   
   
3. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the package:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install .
   ```

## Usage

Here's a basic example of how to use DobyEmail to send an email:

```python
from dobyemail import Service, config

# Initialize the email service
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
to_email = "recipient@example.com"
subject = "Test Email"
body = "This is a test email sent using DobyEmail."
service.send_email(to_email, subject, body)

# Read emails
emails = service.read_emails(limit=5)
for email in emails:
    print(f"From: {email['from']}, Subject: {email['subject']}")

# Validate an email address
from dobyemail import is_valid_email
print(is_valid_email("test@example.com"))  # True

# Parse a date string
from dobyemail import parse_date
print(parse_date("2023-05-15"))  # "15-May-2023"
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

This project is licensed under the MIT License - see the LICENSE file for details.
