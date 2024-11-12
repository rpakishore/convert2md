#!/bin/bash

# Navigate to the directory of the script, then up two levels
cd "$(dirname "$0")"
cd ../..

# Check if pyproject.toml exists
if [[ ! -f "pyproject.toml" ]]; then
    echo "Error: pyproject.toml not found in the current directory."
    exit 1
else
    echo "pyproject.toml found. Continuing with the script."
fi

# Install 'uv' if not already installed, then run the specified Python script
pip3 install uv
uv run scripts/main.py
