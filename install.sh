#!/bin/bash

# Update/Upgrade apt packages
sudo apt update 

# Install Pyenv dependencies. This is to ensure the right version of Python is used
sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y

# Install Pyenv
curl https://pyenv.run | bash

# Add To Bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

# Add to Bashprofile
touch ~/.profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init - bash)"' >> ~/.profile

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

chmod +x run.sh

# Run App
sh run.sh
