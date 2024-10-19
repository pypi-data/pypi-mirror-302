import os
import re

from setuptools import setup, find_packages

# Check if src/__init__.py exists
if not os.path.exists("src/__init__.py"):
    raise FileNotFoundError("src/__init__.py not found. Make sure it exists and contains the version information.")

# Read version from __init__.py
with open("src/__init__.py") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    )[1]

# Read long description
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="transformers_modules",
    version=version,
    author="",
    author_email="",
    description="A short description of the package",  # Add a short description here
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where="src"),  # This will find all packages in the src directory
    package_dir={"": "src"},
    install_requires=install_requires,
    python_requires=">= 3.8, != 3.11.*",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)

# After setup, print some debug information
print(f"Package name: transformers_modules")
print(f"Version: {version}")
print(f"Packages: {find_packages(where='src')}")
print(f"Install requires: {install_requires}")