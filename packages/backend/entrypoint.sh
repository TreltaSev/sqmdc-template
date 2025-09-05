#!/bin/sh
set -e

exec /opt/venv/bin/python -u /backend/src/main.py "$@"