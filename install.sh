#!/bin/bash
# JARVIS Global Command Installer

echo "Installing JARVIS globally..."

# Get the absolute path to the jarvis directory
JARVIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Compiling biometric security modules..."
swiftc "$JARVIS_DIR/core/auth.swift" -o "$JARVIS_DIR/core/jarvis_auth" 2>/dev/null || echo "Warning: Could not compile biometrics. Skipping..."

echo "Checking system dependencies..."
if command -v brew &> /dev/null; then
    brew install portaudio --quiet
else
    echo "Homebrew not found. Voice input (PyAudio) might fail to install."
fi

echo "Building Python virtual environment..."
python3 -m venv "$JARVIS_DIR/venv"
source "$JARVIS_DIR/venv/bin/activate"

echo "Installing neural dependencies..."
pip install -r "$JARVIS_DIR/requirements.txt" --quiet

# Create the executable wrapper
cat << 'EOF' > "$JARVIS_DIR/jarvis_cmd"
#!/bin/bash
# Find where the script is located
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Activate venv and run
source "$DIR/venv/bin/activate"
python3 "$DIR/main.py" "$@"
EOF

# Make it executable
chmod +x "$JARVIS_DIR/jarvis_cmd"

# Create symlink in /usr/local/bin
echo "Requesting administrator privileges to link command to /usr/local/bin/jarvis"
sudo ln -sf "$JARVIS_DIR/jarvis_cmd" /usr/local/bin/jarvis

if [ $? -eq 0 ]; then
    echo "✅ SUCCESS! You can now type 'jarvis' from anywhere in your terminal!"
else
    echo "❌ Failed to create symlink. Try running: sudo ln -sf $JARVIS_DIR/jarvis_cmd /usr/local/bin/jarvis"
fi
