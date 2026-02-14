#!/bin/bash

# Update/Upgrade apt packages
sudo apt update -y && sudo apt upgrade -y

# Install Tkinter Dependency
echo "Installing TKinter"
sudo apt install python3-tk -y

