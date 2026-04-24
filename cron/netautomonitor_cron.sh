#!/usr/bin/env bash
set -euo pipefail

# Resolve project root from this script location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Runtime paths.
PYTHON_BIN="${PYTHON_BIN:-python3}"
ENTRYPOINT="${PROJECT_ROOT}/src/main.py"
LOG_DIR="${PROJECT_ROOT}/logs"
RUN_LOG="${LOG_DIR}/cron-run.log"

mkdir -p "${LOG_DIR}"

# Run from project root so relative paths in the app work.
cd "${PROJECT_ROOT}"

{
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Starting NetAutoMonitor run"
  "${PYTHON_BIN}" "${ENTRYPOINT}"
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] NetAutoMonitor run finished"
} >> "${RUN_LOG}" 2>&1
