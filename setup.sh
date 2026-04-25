#!/bin/bash
# JARVIS Remote Installer
# Usage: curl -sL https://raw.githubusercontent.com/Avikamggh/JARVIS-Shadow-Protocol/main/setup.sh | bash

set -e

echo -e "\033[1;31m"
echo "█████████████████████████████████████████████████████"
echo "█ ⚠ INITIATING JARVIS SHADOW PROTOCOL INSTALLATION ⚠ █"
echo "█████████████████████████████████████████████████████"
echo -e "\033[0m"

# 1. Check requirements
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is required to install JARVIS."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is required to install JARVIS."
    exit 1
fi

# 2. Clone the repository into ~/.jarvis
INSTALL_DIR="$HOME/.jarvis"

if [ -d "$INSTALL_DIR" ]; then
    echo "🔄 JARVIS is already installed at $INSTALL_DIR. Updating..."
    cd "$INSTALL_DIR"
    git fetch origin main --quiet
    git reset --hard origin/main --quiet
else
    echo "📥 Downloading JARVIS neural core..."
    git clone --quiet https://github.com/Avikamggh/JARVIS-Shadow-Protocol.git "$INSTALL_DIR"
fi

# 3. Trigger the internal installer
echo "⚙️  Building Python environment and system links..."
cd "$INSTALL_DIR"
chmod +x install.sh
sudo ./install.sh

echo ""
echo -e "\033[1;32m✅ INSTALLATION COMPLETE. \033[0m"
echo "You can now boot the system by typing 'jarvis' anywhere in your terminal."
