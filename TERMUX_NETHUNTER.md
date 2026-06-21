# PersonaProbe - Termux/NetHunter Installation Guide

This guide covers installation and usage of PersonaProbe on mobile devices using Termux or NetHunter.

## What is Termux?

**Termux** is an Android terminal emulator and Linux environment app that allows you to run Linux commands and tools on your Android device without rooting.

**NetHunter** is a Kali Linux-based penetration testing platform for Android devices (Nexus, Pixel, OnePlus devices).

## Installation on Termux

### Step 1: Install Termux
- Download from [Google Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/en/packages/com.termux/)
- Open Termux after installation

### Step 2: One-Line Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Brianmcnabb508/Personaprobe/main/install.sh | bash
```

Or manually:

```bash
apt update && apt upgrade -y
apt install git python3 python3-pip -y
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe
pip install -r requirements.txt
chmod +x personaprobe.py
```

### Step 3: Verify Installation

```bash
python3 setup_verify.py
```

Expected output:
```
[✓] Python version
[✓] Dependencies
[✓] Internet
[✓] Module import

Passed: 4/4
[+] All checks passed!
```

## Installation on NetHunter

### Step 1: Install NetHunter
- Follow official NetHunter installation guide
- NetHunter typically includes most tools pre-installed

### Step 2: Quick Installation

```bash
apt update
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe
pip install -r requirements.txt
chmod +x personaprobe.py
```

## Basic Usage

### Simple Domain Lookup
```bash
python3 personaprobe.py -d example.com
```

### Person Investigation
```bash
python3 personaprobe.py -n "John Doe" -u johndoe123
```

### Email Breach Check
```bash
python3 personaprobe.py -e admin@company.com
```

### Full Reconnaissance
```bash
python3 personaprobe.py -d company.com -n "CEO Name" --verbose
```

### Help Menu
```bash
python3 personaprobe.py -h
```

## API Key Setup (Termux)

### 1. Get HaveIBeenPwned API Key
- Visit https://haveibeenpwned.com/API/Key
- Register and get your API key

### 2. Set Environment Variable
```bash
export HIBP_APIKEY="your_api_key_here"
```

### 3. Make it Persistent (Termux)
```bash
# Edit your Termux profile
nano ~/.bashrc

# Add this line at the end:
export HIBP_APIKEY="your_api_key_here"

# Save: Ctrl+O, Enter, Ctrl+X
# Reload:
source ~/.bashrc
```

## Performance Optimization for Mobile

### Use Less Verbose Mode
```bash
# Faster execution
python3 personaprobe.py -d example.com
```

### Check Specific Data Only
```bash
# Just check if website is up
python3 personaprobe.py -d example.com
```

### Monitor Resource Usage
```bash
# In another terminal, check resource usage
watch -n 1 'ps aux | grep personaprobe'
```

### Reduce Logging Impact
```bash
# Don't use --verbose on low-end devices
python3 personaprobe.py -d example.com
```

## Troubleshooting on Mobile

### Issue: "pip: command not found"
```bash
# Use python3 -m pip instead
python3 -m pip install -r requirements.txt
```

### Issue: "Module not found"
```bash
# Reinstall with force
pip install --force-reinstall requests whois
```

### Issue: "Storage full"
```bash
# Clear cache
rm personaprobe.log
# Or reduce logging to different directory
export PERSONAPROBE_LOG="/sdcard/personaprobe.log"
```

### Issue: "Network timeout"
```bash
# Increase timeout (edit personaprobe.py)
# Change: TIMEOUT = 10
# To: TIMEOUT = 30
```

### Issue: "Permission denied"
```bash
chmod +x personaprobe.py
```

### Issue: Slow performance
```bash
# Check available RAM
free -h

# Kill other apps and try again
```

## File Storage on Mobile

### Termux Storage
```bash
# Your home directory
~/Personaprobe/

# Access Android storage
~/storage/
```

### View Logs
```bash
# From Personaprobe directory
cat personaprobe.log

# Real-time log monitoring
tail -f personaprobe.log
```

### Export Results
```bash
# Copy log to Download folder
cp personaprobe.log ~/storage/downloads/
```

## Networking on Mobile

### WiFi Connection
- Most accurate results with WiFi
- Public WiFi may have rate limiting

### Mobile Data
- Works but may be slower
- Better for quick checks

### VPN Usage
```bash
# Enable VPN first through Android settings
# Then run PersonaProbe normally
python3 personaprobe.py -d example.com
```

## Tips & Tricks

### Create Alias (Termux)
```bash
alias probe="python3 ~/Personaprobe/personaprobe.py"

# Then use:
probe -d example.com
```

### Background Execution
```bash
# Run in background and log to file
nohup python3 personaprobe.py -d example.com > output.txt 2>&1 &

# Check status
jobs
```

### Multiple Targets
```bash
# Create a list
echo "example.com" > targets.txt
echo "example.org" >> targets.txt

# Process each
while read domain; do
    python3 personaprobe.py -d "$domain"
done < targets.txt
```

## Security Considerations

### On Mobile Devices
1. **Don't use public WiFi** for sensitive targets
2. **Use VPN** for additional privacy
3. **Check logs regularly** for sensitive data
4. **Keep Termux updated** - Run `apt update && apt upgrade`
5. **Use strong API keys** - Don't hardcode in files
6. **Clear logs** after sensitive operations

## FAQs

**Q: Can I use PersonaProbe on iOS?**
A: Not directly. You'd need to use remote SSH access to a Linux machine.

**Q: Will this drain my battery?**
A: Web requests and WHOIS lookups use minimal power. Network is the main consumer.

**Q: Can I run multiple instances?**
A: Yes, but be aware of API rate limits.

**Q: How do I uninstall?**
A: Simply delete the directory:
```bash
rm -rf ~/Personaprobe/
```

**Q: Can I update PersonaProbe on mobile?**
A: Yes:
```bash
cd ~/Personaprobe
git pull origin main
pip install -r requirements.txt --upgrade
```

## Getting Help

### Run Verification
```bash
python3 setup_verify.py
```

### Check Logs
```bash
cat personaprobe.log | tail -20
```

### Test Dependencies
```bash
python3 -c "import requests; import whois; print('OK')"
```

### View Manual
```bash
python3 personaprobe.py -h
```

## Next Steps

1. ✅ Installation complete
2. 📖 Read [README.md](README.md) for full documentation
3. 🚀 Run first scan: `python3 personaprobe.py -d github.com`
4. 📝 Check logs: `tail -f personaprobe.log`
5. 🔑 Set up API key for breach checking

---

**Happy Hunting on Mobile! 🔍📱**