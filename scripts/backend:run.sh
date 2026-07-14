#!/usr/bin/env bash
set -euo pipefail

set -a
. "$(dirname $0)/../.env"
set +a

exec "$(dirname $0)/../.venv/bin/uvicorn" src.main.main:app \
  --host 0.0.0.0 \
  --port 8300 \
  --reload \
  --reload-exclude './alembic' \
  --reload-exclude './alembic/*' \
  --reload-exclude './alembic/versions/*' \
  --access-log