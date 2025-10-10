#!/usr/bin/env bash
# rocket.sh - full automation: clean, sync, install, run, test, commit, push
set -euo pipefail
BRANCH="main"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$PROJECT_DIR"
echo "🚀 rocket.sh starting in $PROJECT_DIR"

# 1) Clean pip cache & pyc
echo "🧹 Cleaning caches and bytecode..."
pip cache purge || true
find . -type d -name "__pycache__" -exec rm -rf {} + || true
find . -type f -name "*.pyc" -delete || true

# remove temp files created by scripts
rm -f current.txt to_remove.txt || true

# 2) Safe git pull with stash if necessary
echo "🔄 Syncing with remote..."
if [[ -n "$(git status --porcelain)" ]]; then
  echo "⚠️ Uncommitted changes found. Stashing..."
  git stash push -u -m "auto-stash before rocket.sh"
  STASHED=1
else
  STASHED=0
fi

git fetch origin "$BRANCH"
# prefer rebase for cleaner history
git pull --rebase origin "$BRANCH" || git pull origin "$BRANCH"

if [[ "$STASHED" -eq 1 ]]; then
  echo "🔁 Applying stash..."
  git stash pop || echo "⚠️ stash pop failed — please resolve manually"
fi

# 3) Install dependencies (create virtualenv if needed)
if [[ ! -d ".venv" ]]; then
  echo "🛠 Creating virtualenv .venv..."
  python -m venv .venv
fi
# activate venv for this shell session
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt

# 4) Remove extra packages not in requirements (optional)
echo "🔎 Pruning packages not listed in requirements..."
pip freeze > current.txt
grep -vxFf requirements.txt current.txt > to_remove.txt || true
if [[ -s to_remove.txt ]]; then
  echo "📦 Removing extras: "
  cat to_remove.txt
  pip uninstall -y -r to_remove.txt || true
fi

# 5) Init DB & run app
echo "🗄 Initializing database..."
python - <<'PY'
from app.db import init_db
init_db()
print("DB initialized.")
PY

echo "▶ Running main scraper (offline mode default)..."
python main.py --offline || true

# 6) Run tests
echo "🧪 Running tests..."
pytest -q || echo "⚠️ Some tests failed (see pytest output)."

# 7) Commit any new changes (e.g., new DB entries should not be committed if DB file is in .gitignore)
echo "📁 Committing and pushing changes..."
git add -A
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Auto-update: $(date -u +"%Y-%m-%d %H:%M:%SZ")"
  git push origin "$BRANCH"
fi

echo "✅ rocket.sh finished. Run 'crontab -e' or Termux job scheduler to automate."

