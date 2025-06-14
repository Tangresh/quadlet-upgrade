#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${0}")"; pwd)"

cd "$SCRIPT_DIR" || exit

python -m venv .venv
source "$SCRIPT_DIR"/.venv/bin/activate

python -m pip install -r requirements.txt
