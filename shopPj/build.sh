#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
source .venv/bin/activate
pip install -r requirements.txt

# Convert static asset files
python ./shopPj/manage.py collectstatic --no-input

# Apply any outstanding database migrations
python ./shopPj/manage.py migrate
