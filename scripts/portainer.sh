#!/bin/bash
# Portainer manager CLI wrapper — short, reliable, LLM-friendly
# Usage: portainer <command> [args...]
# Path: /opt/data/skills/portainer/scripts/portainer.sh

VENV_PYTHON="/opt/data/venv/bin/python3"
SCRIPT="/opt/data/skills/portainer/scripts/portainer_manager.py"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Python venv not found at $VENV_PYTHON" >&2
    echo "Run: cd /opt/data && python3 -m venv venv && venv/bin/pip install requests urllib3" >&2
    exit 1
fi

exec "$VENV_PYTHON" "$SCRIPT" "$@"