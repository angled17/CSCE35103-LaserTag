#!/usr/bin/env bash

source .venv/bin/activate
export PYGAME_HIDE_SUPPORT_PROMPT=1

cd src
python main.py $@