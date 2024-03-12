@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check for Chocolatey and install if not present
where /q choco
if %ERRORLEVEL% neq 0 (
    echo Chocolatey not found. Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    echo Please restart your PowerShell session to complete the Chocolatey installation.
    exit /b
) else (
    echo Chocolatey is already installed.
)

:: Clear the screen
cls

:: Install Git and Python using Chocolatey
echo Installing Git...
choco install git -y
if %ERRORLEVEL% neq 0 exit /b
echo Git installation completed. A reboot may be required.

echo Installing Python...
choco install python --version=3.11 -y
if %ERRORLEVEL% neq 0 exit /b
echo Python installation completed.

Echo Installing ffmpeg...
choco install ffmpeg
if %ERRORLEVEL% neq 0 exit /b
echo ffmpeg installation completed.

:: Suggest reboot here if Git was installed for the first time
echo A reboot is recommended to ensure all changes take effect. Please reboot your system and rerun the script if necessary.

:: Pause here to let the user decide on reboot
pause

:: Change directory to the script's directory
cd /d "%~dp0"

:: Install Python dependencies, ensuring 'wheel' is installed first
echo Installing Python dependencies...
pip install wheel
pip install requests openai spotipy SpeechRecognition gTTS pydub PyAudio pvporcupine socketio sympy setuptools BeautifulSoup
echo Python dependencies installation completed.
echo Installing Electron...
call npm install electron
if %ERRORLEVEL% neq 0 exit /b
echo Electron install completed.

echo Setup completed.

call npm start