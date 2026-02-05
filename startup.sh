#!/bin/bash
set -e

# ===== Teams AI Bot startup script =====

# venv path
VENV_DIR=".venv"

# ensure log dir exists
mkdir -p /home/site/wwwroot

# create timestamped logfile (no overwrite, no append)
LOGFILE="/home/site/wwwroot/teams-ai-bot-$(date +%Y%m%d-%H%M%S).log"

echo "Starting Teams AI Bot with gunicorn..."
echo "Log file: $LOGFILE"

exec "$VENV_DIR/bin/gunicorn" app:app   --worker-class aiohttp.GunicornWebWorker   --bind "0.0.0.0:${PORT}"   --access-logfile "$LOGFILE"   --error-logfile "$LOGFILE"   --access-logformat '%(m)s %(U)s -> %(s)s'   --log-level info   --capture-output
