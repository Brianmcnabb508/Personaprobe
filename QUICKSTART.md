# Quick Start Guide for PersonaProbe

## Installation (All Platforms)

### Automatic Installation (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/Brianmcnabb508/Personaprobe/main/install.sh | bash
```

Or:

```bash
wget https://raw.githubusercontent.com/Brianmcnabb508/Personaprobe/main/install.sh -O install.sh
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x personaprobe.py
```

## Quick Start

### 1. Set API Key (Optional)
```bash
export HIBP_APIKEY="your_api_key_here"
```

### 2. Run PersonaProbe
```bash
python3 personaprobe.py -d example.com
```

## Common Usage Examples

### Search by Domain
```bash
python3 personaprobe.py -d github.com
```

### Search by Name
```bash
python3 personaprobe.py -n "John Doe"
```

### Search by Username
```bash
python3 personaprobe.py -u johndoe123
```

### Search by Email
```bash
python3 personaprobe.py -e admin@company.com
```

### Combined Search
```bash
python3 personaprobe.py -d company.com -n "CEO Name" -u ceo123 --verbose
```

### Verbose Mode (Detailed Logging)
```bash
python3 personaprobe.py -d example.com --verbose
```

## Platform-Specific Notes

### Termux
```bash
# Install Termux (from Google Play or F-Droid)
# Open Termux and run:
curl -fsSL https://raw.githubusercontent.com/Brianmcnabb508/Personaprobe/main/install.sh | bash
```

### NetHunter
```bash
# Automatically available in most NetHunter installations
# Just run the install script above
```

### Kali Linux / ParrotOS / Debian
```bash
sudo apt update
sudo apt install git python3-pip
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe
pip install -r requirements.txt
```

## Troubleshooting

### Python Not Found
```bash
# Try python3 explicitly
python3 personaprobe.py -d example.com
```

### Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Permission Denied
```bash
chmod +x personaprobe.py
```

### API Key Not Working
```bash
# Verify key is set
echo $HIBP_APIKEY

# Set it if missing
export HIBP_APIKEY="your_key"
```

## File Structure

```
Personaprobe/
├── personaprobe.py          # Main tool
├── requirements.txt          # Dependencies
├── requirements-dev.txt      # Testing dependencies
├── test_personaprobe.py     # Test suite
├── pytest.ini               # Test configuration
├── TESTING.md               # Testing guide
├── install.sh               # Installation script
├── QUICKSTART.md            # This file
├── README.md                # Full documentation
└── personaprobe.log         # Log file (created on first run)
```

## Output Files

- **personaprobe.log** - All operations and results logged here
- Check logs for detailed information about each scan

## Help & Support

```bash
python3 personaprobe.py -h
```

For more information, see [README.md](README.md) and [TESTING.md](TESTING.md)