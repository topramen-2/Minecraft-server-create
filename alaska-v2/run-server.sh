#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if command -v python3 >/dev/null && python3 -c 'import tomllib' 2>/dev/null; then
  exec python3 manage.py "$@"
fi
# Fallback for ZimaOS without Python 3.11+. The helper only needs /DATA and Docker's local socket.
exec docker run --rm -i \
  -v /DATA:/DATA \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD":/kit -w /kit \
  python:3.12-slim python manage.py "$@"
