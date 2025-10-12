#!/bin/bash
# auto_backup.sh - Automatically save conversation to GitHub

# Configuration
REPO_DIR="/path/to/my_project"
CONV_DIR="$REPO_DIR/conversations"
FILE_NAME="chat_$(date +'%Y-%m-%d_%H-%M-%S').txt"
GITHUB_BRANCH="main"

# Make sure conversations folder exists
mkdir -p "$CONV_DIR"

# Save conversation input
echo "Paste your conversation (end with Ctrl+D):"
cat > "$CONV_DIR/$FILE_NAME"

# Change to repo directory
cd "$REPO_DIR" || exit

# Add, commit, and push
git add "$CONV_DIR/$FILE_NAME"
git commit -m "Backup conversation: $FILE_NAME"
git push origin "$GITHUB_BRANCH"

echo "✅ Conversation backed up to GitHub as $FILE_NAME"
