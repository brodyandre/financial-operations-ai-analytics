#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python3 -m taranis_black.audit
python3 -m unittest discover -s tests -v
