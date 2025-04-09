#!/bin/bash
# Launcher script for Tetris for Mac

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the game directory
cd "$DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not found. Please install Python 3 from python.org" buttons {"OK"} default button "OK" with icon stop with title "Python Not Found"'
    exit 1
fi

# Check if Pygame is installed
if ! python3 -c "import pygame" &> /dev/null; then
    osascript -e 'display dialog "Pygame is required but not found. Installing Pygame..." buttons {"OK"} default button "OK" with title "Installing Pygame"'
    pip3 install pygame
    
    # Check if installation was successful
    if ! python3 -c "import pygame" &> /dev/null; then
        osascript -e 'display dialog "Failed to install Pygame. Please install it manually with: pip3 install pygame" buttons {"OK"} default button "OK" with icon stop with title "Installation Failed"'
        exit 1
    fi
fi

# Run the game
python3 "$DIR/main_optimized.py"
