#!/bin/bash
# ╔══════════════════════════════════════════════════╗
# ║           JARVIS Launch Script                    ║
# ║   Just A Rather Very Intelligent System           ║
# ╚══════════════════════════════════════════════════╝

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "  ⚠  GEMINI_API_KEY not set!"
    echo ""
    echo "  Get your free API key at: https://aistudio.google.com/apikey"
    echo ""
    echo "  Then run:"
    echo "    export GEMINI_API_KEY='your-key-here'"
    echo "    ./start.sh"
    echo ""
    echo "  Or add it permanently to your shell:"
    echo "    echo \"export GEMINI_API_KEY='your-key-here'\" >> ~/.zshrc"
    echo ""
    exit 1
fi

# Launch JARVIS
python3 "$SCRIPT_DIR/main.py" "$@"
