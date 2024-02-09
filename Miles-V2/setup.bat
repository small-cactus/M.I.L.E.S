@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check for Chocolatey and install if not present
where /q choco
if %ERRORLEVEL% neq 0 (
    echo Chocolatey not found. Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    echo Chocolatey installed.
) else (
    echo Chocolatey is already installed.
)

:: Clear the screen
cls

:: Install Git, Python, and Node.js using Chocolatey
echo Installing Git...
choco install git -y
echo Git installation completed.

echo Installing Python...
choco install python --version=3.11 -y
echo Python installation completed.

echo Installing Node.js...
choco install nodejs -y
echo Node.js installation completed.

:: Change directory to the script's directory
cd /d "%~dp0"

:: Install Python dependencies
echo Installing Python dependencies...
pip install requests openai spotipy SpeechRecognition gTTS pydub PyAudio pvporcupine socketio winsound platform
echo Python dependencies installation completed.

:: Install Node.js dependencies
echo Installing Node.js dependencies...
npm install
npm install electron
echo Node.js dependencies installation completed.

:: Start the Node.js application
echo Starting the Node.js application...
npm start

echo Setup and launch completed.