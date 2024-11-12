@echo off

rem Change the current working directory to the directory of the batch script
cd /d %~dp0
cd ..\..

if not exist pyproject.toml (
    echo "Error: pyproject.toml not found in the current directory."
    exit /b 1
) else (
    echo "pyproject.toml found. Continuing with the script."
)

rem Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python needs to be installed for this script to work
    pause
    exit /b 1
)

rem Install uv and use uv to run script
pip install uv
uv run scripts/main.py