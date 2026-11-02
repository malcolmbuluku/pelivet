#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then python -m venv .venv 2>/dev/null || py -3 -m venv .venv; fi
if [ -f .venv/Scripts/activate ]; then source .venv/Scripts/activate; else source .venv/bin/activate; fi
pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
python seed.py
echo ">> PELIVET running at http://127.0.0.1:5000  (admin at /admin)"
python app.py
