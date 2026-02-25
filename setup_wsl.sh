#!/bin/bash
# Setup script for WSL2 - APK building with buildozer
# This script sets up the environment to build Android APKs

set -e  # Exit on error

echo "Setting up Elixir Technology project for Android APK building..."
echo ""

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt install -y python3-full python3-venv python3-pip git zip unzip

# Create virtual environment
VENV_PATH="$HOME/.venv-elixir"
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
else
    echo "Virtual environment already exists at $VENV_PATH"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install buildozer and dependencies
echo "Installing buildozer and dependencies..."
pip install buildozer cython==0.29.37 kivy==2.3.0 kivymd==1.2.0

echo ""
echo "Setup complete!"
echo ""
echo "To use this environment in the future, run:"
echo "  source $VENV_PATH/bin/activate"
echo ""
echo "Then build APK with:"
echo "  cd /mnt/c/Users/erbay/OneDrive/Belgeler/GitHub/yeter"
echo "  buildozer android debug"
echo ""
