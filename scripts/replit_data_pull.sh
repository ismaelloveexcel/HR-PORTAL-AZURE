#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_DIR="${1:-$ROOT_DIR/exports}"

mkdir -p "$EXPORT_DIR"

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "DATABASE_URL is not set. Configure it in Replit Secrets before running."
  exit 1
fi

if [[ ! "$DATABASE_URL" =~ ^postgres(ql)?(\+asyncpg)?:// ]]; then
  echo "DATABASE_URL must be a PostgreSQL connection string."
  exit 1
fi

fail_dump() {
  echo "$1 (check DATABASE_URL and permissions)."
  exit 1
}

echo "📥 Exporting PostgreSQL data from Replit (this can take a moment on larger datasets)..."
EXPORT_PLAIN_SQL=${EXPORT_PLAIN_SQL:-1}
pg_dump "$DATABASE_URL" -Fc -f "$EXPORT_DIR/replit_db.dump" || fail_dump "Database export failed for custom format -> $EXPORT_DIR/replit_db.dump"
if [[ "$EXPORT_PLAIN_SQL" -eq 1 ]]; then
  pg_dump "$DATABASE_URL" -f "$EXPORT_DIR/replit_db.sql" || fail_dump "Database export failed for plain SQL -> $EXPORT_DIR/replit_db.sql"
else
  echo "ℹ️  Skipping plain SQL export (set EXPORT_PLAIN_SQL=1 to enable)."
fi

echo "🗂️  Capturing lightweight app snapshot..."
APP_ITEMS=(backend frontend README.md replit.md .replit)
SNAPSHOT_ITEMS=()
for item in "${APP_ITEMS[@]}"; do
  if [[ -e "$ROOT_DIR/$item" ]]; then
    SNAPSHOT_ITEMS+=("$item")
  else
    echo "ℹ️  Skipping missing path in snapshot: $item"
  fi
done
if [[ ${#SNAPSHOT_ITEMS[@]} -gt 0 ]]; then
  tar -czf "$EXPORT_DIR/app_snapshot.tar.gz" -C "$ROOT_DIR" "${SNAPSHOT_ITEMS[@]}"
else
  echo "⚠️  No files available for the app snapshot archive."
fi

echo "🔎 Running code analysis (full health scan)..."
SCAN_SCRIPT="$ROOT_DIR/scripts/proactive_scan.py"
PYTHON_BIN=""
for python_cmd in python3 python; do
  if command -v "$python_cmd" >/dev/null 2>&1; then
    PYTHON_BIN="$python_cmd"
    break
  fi
done
if [[ -z "$PYTHON_BIN" ]]; then
  echo "⚠️  No Python interpreter found; skipping proactive scan."
elif [[ -f "$SCAN_SCRIPT" ]]; then
  if "$PYTHON_BIN" "$SCAN_SCRIPT" --full; then
    echo "ℹ️  Proactive scan completed."
  else
    echo "⚠️  Proactive scan exited with a non-zero status (report may be partial)."
  fi
  if [[ -f "$ROOT_DIR/scan_report.json" ]]; then
    cp "$ROOT_DIR/scan_report.json" "$EXPORT_DIR/"
  fi
else
  echo "ℹ️  Scan script not found at $SCAN_SCRIPT; skipping proactive scan."
fi

echo "✅ Data pull complete. Download artifacts from the Replit Files panel in: $EXPORT_DIR"
