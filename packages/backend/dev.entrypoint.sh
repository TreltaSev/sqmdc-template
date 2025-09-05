#!/bin/sh
set -e

exec /opt/venv/bin/watchmedo auto-restart --patterns=*.py --recursive -- /opt/venv/bin/python -u /backend/src/main.py "$@"