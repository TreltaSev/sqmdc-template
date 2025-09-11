#!/bin/sh
set -e

exec /opt/venv/bin/python -u /tools/src/main.py "$@"