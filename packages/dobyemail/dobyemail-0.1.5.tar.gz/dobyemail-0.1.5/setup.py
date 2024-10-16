from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dobyemail",
    version="0.1.5",  # Incrementing the version number
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    description="Do By Email is a comprehensive Python package for handling various email operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://python.dobyemail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
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
