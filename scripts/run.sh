#!/usr/bin/env bash
# simple runner
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python main.py --once
# to run dashboard: python run_dashboard.py
