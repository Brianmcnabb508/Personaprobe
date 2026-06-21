#!/bin/bash

# PersonaProbe Installation Script
# Supports: Linux, Termux, NetHunter, Kali Linux, ParrotOS

echo "=========================================="
echo "  PersonaProbe Installation Script"
echo "=========================================="
echo ""

# Detect OS/Environment
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s)
fi

echo "[*] Detected OS/Environment: $OS"

# Check if running on Termux
if [ -d "$PREFIX" ]; then
    echo "[*] Detected Termux environment"
    IS_TERMUX=1
else
    IS_TERMUX=0
fi

# Update package manager
echo "[+] Updating package manager..."
if command -v apt-get &> /dev/null; then
    apt-get update -y
    apt-get upgrade -y
elif command -v apt &> /dev/null; then
    apt update -y
    apt upgrade -y
elif command -v pacman &> /dev/null; then
    pacman -Syu --noconfirm
fi

# Install Python 3 and dependencies
echo "[+] Installing Python 3 and dependencies..."
if command -v apt-get &> /dev/null; then
    apt-get install -y python3 python3-pip python3-dev git
elif command -v apt &> /dev/null; then
    apt install -y python3 python3-pip python3-dev git
elif command -v pacman &> /dev/null; then
    pacman -S --noconfirm python python-pip git base-devel
fi

# Verify Python installation
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 installation failed!"
    exit 1
fi

echo "[+] Python 3 installed successfully"
python3 --version

# Clone or navigate to PersonaProbe
if [ ! -d "Personaprobe" ]; then
    echo "[+] Cloning PersonaProbe repository..."
    git clone https://github.com/Brianmcnabb508/Personaprobe.git
    cd Personaprobe
else
    echo "[*] PersonaProbe directory already exists"
    cd Personaprobe
fi

# Upgrade pip
echo "[+] Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip install -r requirements.txt

# Verify installations
echo ""
echo "[+] Verifying installations..."
python3 -c "import requests; print('[+] requests module installed')" || echo "[!] requests installation failed"
python3 -c "import whois; print('[+] whois module installed')" || echo "[!] whois installation failed"

# Make script executable
echo "[+] Making script executable..."
chmod +x personaprobe.py

# Create symlink for easy access (optional)
if [ -w "/usr/local/bin" ]; then
    echo "[+] Creating symlink in /usr/local/bin..."
    ln -sf "$(pwd)/personaprobe.py" /usr/local/bin/personaprobe
    echo "[+] You can now run 'personaprobe' from anywhere"
fi

# Installation complete
echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "[+] PersonaProbe is ready to use!"
echo ""
echo "Next steps:"
echo "  1. Set up HaveIBeenPwned API key (optional):"
echo "     export HIBP_APIKEY='your_api_key'"
echo ""
echo "  2. Run PersonaProbe:"
echo "     python3 personaprobe.py -h"
echo ""
echo "  3. Example usage:"
echo "     python3 personaprobe.py -d example.com -n 'John Doe'"
echo ""
echo "For detailed instructions, see README.md"
echo "=========================================="