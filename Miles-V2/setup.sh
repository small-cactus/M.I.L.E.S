#!/bin/bash

# Total number of tasks to perform
TOTAL_TASKS=7 # Homebrew check, Homebrew installation, Git, Python 3.11, Node.js, Python dependencies, Node.js dependencies
COMPLETED_TASKS=0

# Function to update progress and clear the screen
update_progress() {
    clear
    COMPLETED_ACTION=$1
    ((COMPLETED_TASKS++))
    PERCENTAGE=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))
    echo "$COMPLETED_ACTION completed. Progress: $PERCENTAGE%. Continuing in 3 seconds..."
    sleep 3
    clear
}

# Function to install a Homebrew package if it's not already installed
install_if_not_present() {
    PACKAGE=$1
    if ! command -v $PACKAGE &> /dev/null
    then
        echo "Installing $PACKAGE..."
        brew install $PACKAGE
        update_progress "Installation of $PACKAGE"
    else
        echo "$PACKAGE is already installed."
        update_progress "$PACKAGE verification"
    fi
}

# Clear the screen initially
clear

# Check if Homebrew is installed
echo "Checking Homebrew installation..."
if ! command -v brew &> /dev/null
then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    update_progress "Homebrew installation"
else
    echo "Homebrew is already installed."
    update_progress "Homebrew verification"
fi

# Install Git, Python 3.11, Node.js
install_if_not_present git
install_if_not_present python@3.11
install_if_not_present node

# Change directory to the script's directory
cd "$(dirname "$0")" || exit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install requests openai spotipy SpeechRecognition gTTS pydub PyAudio openwakeword socketio sympy setuptools bs4 TensorFlow
update_progress "Python dependencies installation"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install
update_progress "Node.js dependencies installation"

echo "Downloading Wake Word model for 'Miles'..."
python3 download-model.py

# Start the Node.js application
echo "Starting the Node.js application..."
npm start

echo "Setup and launch completed."
