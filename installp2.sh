#!/usr/bin/env bash -i

source ~/.bashrc

# Install Python 3.11.2
pyenv install 3.11.2
pyenv shell 3.11.2

# Install Tkinter
sudo apt install python3-tk -y

# Create Virtual Environment
python -m venv .venv

# Activate venv and install requirements
source .venv/bin/activate
pip install -r "requirements.txt"

# Run App
./run.sh