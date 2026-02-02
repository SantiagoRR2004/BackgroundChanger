#!/bin/bash

# First create a virtual environment
python3 -m venv .venv

# Then activate it
source .venv/bin/activate

# Finally install the required packages
pip install -r requirements.txt
