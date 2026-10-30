#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
docker info >/dev/null
docker compose up -d ollama ledger
docker compose exec -T ollama ollama pull qwen2.5:3b
docker compose run --rm n8n import:workflow --input=/workflows/supplier-delay-triage.json
docker compose run --rm n8n execute --id=supplierDelayCapstone2026 --rawOutput
printf '\nResults: http://127.0.0.1:8091/results\nCSV: http://127.0.0.1:8091/results.csv\n'
