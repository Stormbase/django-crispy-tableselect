#!/bin/sh

# This script is used to update and manage translations.
# Usage:
#
# Update all languages:
# ./update_translations.sh --all
#
# Create or update existing language:
# ./update_translations.sh -l <language_code>

set -e

echo "\nUpdating django.po files..."
# Update Django translations
python manage.py makemessages --ignore venv --ignore .tox -d django --no-obsolete $@
