@echo off
:: Check if a path is provided as an argument
if "%~1"=="" (
    echo Please provide a path as an argument.
    exit /b 1
)

:: Change directory to the provided path
cd /d "%~1"
if %errorlevel% neq 0 (
    echo Failed to change directory. Please ensure the path is correct.
    exit /b 1
)

:: Run the uv command with the specified arguments
uv add --dev pre-commit
