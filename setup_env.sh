#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch CPU-only first to avoid CUDA bloat
echo "Installing PyTorch (CPU only)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
echo "Installing other dependencies..."
pip install -r requirements.txt

echo "Setup complete. Activate with 'source venv/bin/activate'"
