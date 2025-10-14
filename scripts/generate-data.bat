@echo off
echo ================================================
echo Splunk Intermediate Training - Data Generator
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Running data generation script...
echo.
python "%~dp0data-generators\generate_sample_data.py"

echo.
echo ================================================
echo Data generation complete!
echo ================================================
pause
