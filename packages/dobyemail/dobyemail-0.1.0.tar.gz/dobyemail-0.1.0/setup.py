from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dobyemail",
    version="0.1.0",
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    description="Do By Email is a comprehensive Python package for handling various email operations. It provides a set of utilities and classes to simplify email-related tasks in your Python projects.",
    long_description="Service: Main class that encapsulates both SMTP and IMAP operations, providing a high-level interface for sending and receiving emails. Sender: Handles the composition and sending of emails, including support for attachments. Reader: Manages connections to IMAP servers, fetching emails, and parsing their content. Transfer: Facilitates the movement of emails between different email accounts or folders. Config: Manages configuration settings for the email service, including server addresses, ports, and authentication details. get_email_ports: Retrieves standard email port configurations",
    long_description_content_type="text/markdown",
    url="https://github.com/dobyemail/python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    include_package_data=True,
    package_data={
        "dobyemail": ["email_ports.json"],
    },
)
