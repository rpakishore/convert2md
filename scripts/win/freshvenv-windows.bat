@echo off
echo "Navigating to Root Dir"
cd /d %~dp0
cd ..\..

if not exist pyproject.toml (
    echo "Error: pyproject.toml not found in the current directory."
    exit /b 1
) else (
    echo "pyproject.toml found. Continuing with the script."
)

pip install uv
uv pip install -r pyproject.toml --extra dev

