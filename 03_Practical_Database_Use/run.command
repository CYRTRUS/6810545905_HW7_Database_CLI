#!/bin/bash

cd "$(dirname "$0")" || exit 1

if [ ! -x "./.venv/bin/python" ]; then
    echo "Virtual environment not found."
    echo "Create it with: python3 -m venv .venv"
    echo "Install dependencies with:"
    echo "./.venv/bin/python -m pip install -r requirements.txt"
    exit 1
fi

./.venv/bin/python main.py
