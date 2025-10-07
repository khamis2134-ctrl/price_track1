#!/data/data/com.termux/files/usr/bin/bash
echo "🧹 Cleaning cache..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +
echo "🔧 Reinstalling dependencies..."
pip install -r requirements.txt --upgrade
echo "🚀 Running main.py..."
python main.py
