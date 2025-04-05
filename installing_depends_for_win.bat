@echo off
echo.
echo =====================================================
echo Checking and Installing Prerequisites for NAT Script
echo =====================================================
echo.

:: Check for admin rights
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Warning: This script may require administrative privileges for some operations.
    echo Consider running as Administrator if you encounter problems.
    echo.
)

:: Step 1: Check if Python is installed
echo Checking if Python is installed...
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found! Downloading and installing...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile 'python_installer.exe'}"
    echo Running Python installer. Please follow the prompts...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo Python installed successfully.
)

:: Step 2: Check if Python is in PATH
echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not accessible. Please restart your computer and run this script again.
    pause
    exit /b 1
)

:: Step 3: Upgrade Pip and Setuptools
echo Ensuring Pip is installed and updated...
python -m ensurepip
python -m pip install --upgrade pip setuptools

:: Step 4: Check and install Tkinter
echo Checking if Tkinter is available...
python -c "import tkinter" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Warning: Tkinter could not be verified. It should be included with standard Python. Proceeding anyway...
)

:: Step 5: Install Required Python Packages
echo Installing required Python packages...
python -m pip install --no-cache-dir ldap3 pandas matplotlib openpyxl

:: Step 6: Verify All Installations
echo Verifying installations...
python -c "import ldap3, pandas, matplotlib, tkinter, openpyxl, platform; print('All required modules installed successfully!')" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo One or more modules failed to install. Please check for errors above.
    pause
    exit /b 1
)

:: Step 7: Check NetSh availability for NAT operations
echo Checking NetSh availability for NAT operations...
where netsh >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Warning: NetSh command not found. NAT configuration may not work properly.
) ELSE (
    echo NetSh command found. NAT configuration should work properly.
)

echo.
echo =====================================================
echo Prerequisites installation completed successfully!
echo You can now run the main script.
echo =====================================================
echo.
pause