# PersonaProbe

PersonaProbe is an **OSINT (Open Source Intelligence) information gathering tool** designed for penetration testing, security research, and reconnaissance. It automates the process of gathering information about people and organizations from publicly available sources.

## Features

- 🔍 **Web Presence Detection** - Check if a domain has an active website
- 🌐 **WHOIS Information Retrieval** - Get domain registration details
- 📧 **Email Pattern Generation** - Generate potential email addresses
- 🔗 **Social Media Profile Discovery** - Find profiles across multiple platforms
- 🛡️ **Data Breach Checking** - Check if emails/domains appear in known breaches (HaveIBeenPwned)
- 📝 **Comprehensive Logging** - All operations logged to file for review
- ✅ **Input Validation** - Validates all user inputs before processing
- 🚀 **Mobile Compatible** - Works on Termux and NetHunter

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Internet connection

### On Linux / Kali Linux / ParrotOS

```bash
# Clone the repository
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x personaprobe.py
```

### On Termux (Android)

```bash
# Install Python and pip
apt update && apt upgrade
apt install python git

# Clone the repository
git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x personaprobe.py
```

### On NetHunter (Kali on Android)

```bash
# Same as Termux
apt update && apt upgrade
apt install python3 git

git clone https://github.com/Brianmcnabb508/Personaprobe.git
cd Personaprobe

pip install -r requirements.txt
chmod +x personaprobe.py
```

## Setup API Keys

### HaveIBeenPwned API Key (Optional but Recommended)

To check for data breaches, you need a HaveIBeenPwned API key:

1. Visit https://haveibeenpwned.com/API/Key
2. Sign up or log in
3. Purchase an API key (if required)
4. Set the environment variable:

**On Linux/Mac:**
```bash
export HIBP_APIKEY="your_api_key_here"
```

**On Termux/NetHunter:**
```bash
export HIBP_APIKEY="your_api_key_here"
```

**Make it persistent (add to ~/.bashrc or ~/.bash_profile):**
```bash
echo 'export HIBP_APIKEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Usage

```bash
# Search by domain
python personaprobe.py -d example.com

# Search by name
python personaprobe.py -n "John Doe"

# Search by username
python personaprobe.py -u johndoe123

# Search by email
python personaprobe.py -e john@example.com

# Search with multiple parameters
python personaprobe.py -d example.com -n "John Doe" -u johndoe123
```

### Advanced Usage

```bash
# Verbose mode (detailed logging)
python personaprobe.py -d example.com --verbose

# With all parameters
python personaprobe.py -d example.com -n "John Doe" -u johndoe123 -e john@example.com -v

# Help menu
python personaprobe.py -h
```

### Example Commands

```bash
# Reconnaissance on a company
python personaprobe.py -d google.com

# Investigation of a person
python personaprobe.py -n "Elon Musk" -u elonmusk

# Email investigation
python personaprobe.py -e admin@company.com

# Full reconnaissance
python personaprobe.py -d company.com -n "CEO Name" -u ceoname123 --verbose
```

## Output

PersonaProbe provides output in multiple ways:

1. **Console Output** - Real-time results displayed in the terminal
2. **Log File** - All results saved to `personaprobe.log` for later review
3. **Structured Data** - Clean formatted output with status indicators:
   - `[+]` = Success/Found information
   - `[-]` = Not found/Negative result
   - `[!]` = Warning/Error
   - `[*]` = Info/Note
   - `[?]` = Potential match (requires verification)

### Sample Output

```
╔═══════════════════════════════╗
║     PersonaProbe v1.1         ║
║    by Superintellect          ║
╚═══════════════════════════════╝
- Persona Probe: Information Gathering Tool -

[+] Starting reconnaissance for:
    Domain: example.com

===== WEB PRESENCE =====
[+] Checking web presence for: example.com
[+] Website found at https://example.com (Status: 200)

===== WHOIS INFORMATION =====
[+] Querying WHOIS for example.com
[*] Domain Name: example.com
[*] Registrar: VeriSign Registry...
[*] Creation Date: 1995-08-14
[*] Registrant Country: US

===== EMAIL ADDRESS SEARCH =====
[+] Attempting to find emails for domain example.com (via common patterns)
[?] Potential email: info@example.com
[?] Potential email: support@example.com
[?] Potential email: admin@example.com

===== SOCIAL MEDIA PROFILE DISCOVERY =====
[+] Searching LinkedIn...
[?] Potential LinkedIn search URL: https://www.linkedin.com/search/results/all/?keywords=example.com
...

==================================================
[+] PersonaProbe Complete
[*] Log file saved to: personaprobe.log
==================================================
```

## Information Gathering Modules

### 1. Web Presence Check
Checks if a domain has an active website by attempting HTTP/HTTPS connections.

### 2. WHOIS Information
Retrieves domain registration information including:
- Domain name and registrar
- Creation, expiration, and update dates
- Registrant name and organization
- Contact emails and country

### 3. Email Search
Generates potential email addresses based on:
- Common corporate patterns (info@, support@, admin@)
- Target name patterns (firstname@, firstname.lastname@)
- Domain name

### 4. Social Media Discovery
Generates search URLs for:
- LinkedIn
- Twitter/X
- GitHub
- Facebook
- Reddit
- Instagram

### 5. Data Breach Checking
Checks HaveIBeenPwned API to see if:
- Email addresses appear in known breaches
- Domains have been compromised
- Shows breach name, date, and details

## Testing

PersonaProbe includes comprehensive test coverage:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=personaprobe --cov-report=html

# Run specific test
pytest test_personaprobe.py::TestEmailSearch -v
```

See [TESTING.md](TESTING.md) for detailed testing documentation.

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'requests'`
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: `ModuleNotFoundError: No module named 'whois'`
**Solution:** Install whois module
```bash
pip install whois
```

### Issue: HIBP API returns "Unauthorized"
**Solution:** Check your API key
```bash
echo $HIBP_APIKEY  # Verify key is set
```

### Issue: "Could not connect to domain"
**Solution:** Check internet connection and domain validity
```bash
ping example.com
```

### Issue: Slow performance on mobile
**Solution:** Use specific modules instead of all at once
```bash
# Just check web presence, skip expensive operations
python personaprobe.py -d example.com
```

### Issue: Permission Denied
**Solution:** Make script executable
```bash
chmod +x personaprobe.py
```

## Performance Tips for Mobile

On Termux/NetHunter, performance can be limited. Here are optimization tips:

1. **Use specific targets** - Provide exact domain/email rather than generic searches
2. **Skip unnecessary modules** - Don't run all modules if you only need specific info
3. **Use verbose mode sparingly** - Logging can slow performance on older devices
4. **Check disk space** - Ensure you have enough storage for logs
5. **Monitor memory** - Close other apps before running PersonaProbe

## Dependencies

### Core Dependencies (requirements.txt)
- `requests>=2.28.0` - HTTP library for web requests
- `whois>=0.9.7` - WHOIS lookup functionality
- `python-whois>=0.7.3` - Alternative WHOIS library

### Development Dependencies (requirements-dev.txt)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Code coverage
- `pytest-mock>=3.10.0` - Mocking support
- `requests-mock>=1.9.3` - Mock HTTP requests
- `coverage>=6.0` - Coverage analysis

## Logging

All operations are logged to `personaprobe.log`:

```bash
# View logs
cat personaprobe.log

# Follow logs in real-time
tail -f personaprobe.log

# Search logs for specific term
grep "breach" personaprobe.log
```

## Ethical Considerations

⚠️ **Important Legal Notice:**

PersonaProbe is designed for **lawful and ethical OSINT activities** including:
- Penetration testing (with written authorization)
- Security research
- Competitive intelligence
- Due diligence
- Investigative journalism
- Law enforcement activities (where authorized)

**This tool should NOT be used for:**
- Stalking or harassment
- Unauthorized access to systems
- Privacy violations
- Illegal activities
- Unethical information gathering

**You are responsible for complying with all applicable laws and regulations** in your jurisdiction. Always obtain proper authorization before conducting reconnaissance on any target.

## License

This project is open source. See LICENSE file for details.

## Disclaimer

PersonaProbe is provided "as-is" for educational and authorized security testing purposes. The creators are not responsible for misuse or any damages caused by this tool. Users assume full responsibility for their actions.

## Support

### Getting Help

1. **Check this README** - Most answers are here
2. **Run with `--verbose`** - Get detailed debug info
3. **Check the logs** - Review `personaprobe.log` for details
4. **GitHub Issues** - Report bugs or request features

### Reporting Issues

If you find a bug, please:
1. Run with `--verbose` flag
2. Copy the relevant log lines
3. Create a GitHub issue with details

## Contributing

Contributions welcome! Areas for improvement:
- Additional social media platforms
- More email pattern generation
- Integration with other OSINT tools
- Performance optimizations for mobile
- Additional data sources

## Version History

- **v1.1** (Current) - Added input validation, logging, error handling, mobile optimization
- **v1.0** - Initial release with core OSINT modules

## Author

**Superintellect** - OSINT Tool Development

## References & Resources

- [OWASP OSINT Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HaveIBeenPwned API](https://haveibeenpwned.com/API)
- [WHOIS Protocol](https://tools.ietf.org/html/rfc3912)
- [Mobile Penetration Testing](https://www.owasp.org/index.php/Mobile_top_10)

---

**Happy Hunting! 🔍** Remember to always use this tool responsibly and legally.