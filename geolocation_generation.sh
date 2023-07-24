#!/bin/bash

# Create and activate the virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Ensure pip is installed in the virtual environment
python -m ensurepip --default-pip

# Upgrade pip to the latest version (optional, but recommended)
python -m pip install --upgrade pip

# Install dependencies
pip install -r dependencies.txt

# Run the Python script
python geolocation_generation.py

# Deactivate the virtual environment (optional, if you want to exit the virtual environment after the script execution)
deactivate