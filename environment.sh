#!/bin/bash

SCRIPT_DIR=$(dirname "$0")

# First create a virtual environment
python3 -m venv "$SCRIPT_DIR/.venv"

# Then activate it
source "$SCRIPT_DIR/.venv/bin/activate"

# Finally install the required packages
pip install -r "$SCRIPT_DIR/requirements.txt"
