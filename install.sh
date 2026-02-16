#!/bin/bash

# Update/Upgrade apt packages
sudo apt update 

# Install Pyenv dependencies. This is to ensure the right version of Python is used
sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install Pyenv
curl https://pyenv.run | bash

# Install Python 3.11.2
pyenv install 3.11.2
pyenv shell 3.11.2

# Install Tkinter
sudo apt install python3-tk

# Create Virtual Environment
python -m venv .venv

# Activate venv and install requirements
source .venv/bin/activate
pip install -r "requirements.txt"

chmod +x run.sh

# Run App
sh run.sh