#!/bin/bash

# Function to install a Homebrew package if it's not already installed
install_if_not_present() {
    PACKAGE=$1
    if ! command -v $PACKAGE &> /dev/null
    then
        echo "Installing $PACKAGE..."
        brew install $PACKAGE
    else
        echo "$PACKAGE is already installed."
    fi
}

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Install Git, Python 3.11, Node.js, and npm
install_if_not_present git
install_if_not_present python@3.11
install_if_not_present node

# Change directory to the script's directory
cd "$(dirname "$0")" || exit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install requests openai spotipy SpeechRecognition gTTS pydub PyAudio pvporcupine socketio

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Start the Node.js application
echo "Starting the Node.js application..."
npm start

echo "Setup and launch completed."
