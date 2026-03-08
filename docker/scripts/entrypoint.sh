#!/usr/bin/env bash
# Use the unofficial bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail; export FS=$'\n\t'

uvicorn "${APP_PREFIX}.app:app" \
    --proxy-headers \
    --root-path "${UVICORN_ROOT_PATH:-/}" \
    --forwarded-allow-ips "*" \
    --host 0.0.0.0 \
    --port "${UVICORN_PORT:-5050}"

