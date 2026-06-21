#!/usr/bin/env python3

"""
PersonaProbe - OSINT Information Gathering Tool
Supports: Linux, Termux, NetHunter, Kali Linux, ParrotOS

Quick installation and usage verification script
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print header"""
    print("""
    ╔═══════════════════════════════════════╗
    ║   PersonaProbe Setup & Verification  ║
    ║              v1.1                    ║
    ╚═══════════════════════════════════════╝
    """)

def check_python():
    """Check Python version"""
    print("[*] Checking Python version...")
    version = sys.version_info
    print(f"    Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("[!] Python 3.7+ required!")
        return False
    
    print("[+] Python version OK")
    return True

def check_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"[+] {module_name} installed")
        return True
    except ImportError:
        print(f"[-] {module_name} NOT installed")
        return False

def check_dependencies():
    """Check all dependencies"""
    print("\n[*] Checking dependencies...")
    
    modules = [
        ("requests", "requests"),
        ("whois", "whois"),
        ("argparse", "argparse"),
        ("logging", "logging"),
        ("re", "re"),
        ("urllib", "urllib.parse"),
    ]
    
    all_ok = True
    for module, import_name in modules:
        if not check_module(module, import_name):
            all_ok = False
    
    return all_ok

def check_os():
    """Check operating system"""
    print("\n[*] Checking operating system...")
    
    system = platform.system()
    print(f"    System: {system}")
    print(f"    Platform: {platform.platform()}")
    
    # Check for Termux
    if os.path.exists("/data/data/com.termux"):
        print("[+] Detected: Termux")
        return "Termux"
    
    if system == "Linux":
        if os.path.exists("/data/local/tmp"):
            print("[+] Detected: NetHunter/Android")
            return "NetHunter"
        else:
            print("[+] Detected: Linux")
            return "Linux"
    
    return system

def check_internet():
    """Check internet connectivity"""
    print("\n[*] Checking internet connectivity...")
    
    try:
        response = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        if response.returncode == 0:
            print("[+] Internet connection OK")
            return True
    except:
        pass
    
    # Try alternative check
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("[+] Internet connection OK")
        return True
    except:
        print("[-] Internet connection check failed")
        return False

def check_hibp_key():
    """Check HaveIBeenPwned API key"""
    print("\n[*] Checking HaveIBeenPwned API key...")
    
    api_key = os.environ.get("HIBP_APIKEY")
    if api_key:
        print(f"[+] API key found (length: {len(api_key)})")
        return True
    else:
        print("[-] HIBP_APIKEY not set (optional)")
        print("    To enable data breach checking:")
        print("    export HIBP_APIKEY='your_api_key'")
        return False

def check_permissions():
    """Check file permissions"""
    print("\n[*] Checking file permissions...")
    
    if os.access("personaprobe.py", os.X_OK):
        print("[+] personaprobe.py is executable")
    else:
        print("[-] Making personaprobe.py executable...")
        try:
            os.chmod("personaprobe.py", 0o755)
            print("[+] Set executable permission")
        except:
            print("[!] Could not set executable permission")

def check_logs():
    """Check log file"""
    print("\n[*] Checking log file...")
    
    if os.path.exists("personaprobe.log"):
        size = os.path.getsize("personaprobe.log")
        print(f"[+] Log file exists ({size} bytes)")
    else:
        print("[*] Log file will be created on first run")

def test_import():
    """Test importing main module"""
    print("\n[*] Testing PersonaProbe import...")
    
    try:
        import personaprobe
        print("[+] PersonaProbe module imports successfully")
        return True
    except ImportError as e:
        print(f"[-] Import failed: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False

def print_status(checks):
    """Print overall status"""
    print("\n" + "="*50)
    print("VERIFICATION SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "[✓]" if result else "[✗]"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n[+] All checks passed! PersonaProbe is ready to use.")
        print("\nRun PersonaProbe with:")
        print("  python3 personaprobe.py -h")
        return True
    else:
        print("\n[!] Some checks failed. See errors above.")
        return False

def main():
    """Main verification function"""
    print_header()
    
    checks = []
    
    # Run checks
    checks.append(("Python version", check_python()))
    checks.append(("Dependencies", check_dependencies()))
    check_os()
    checks.append(("Internet", check_internet()))
    checks.append(("HIBP API key", check_hibp_key()))
    check_permissions()
    check_logs()
    checks.append(("Module import", test_import()))
    
    # Print results
    success = print_status(checks)
    
    print("\n" + "="*50)
    
    if not success:
        print("\n[*] To fix missing dependencies:")
        print("  pip install -r requirements.txt")
    
    print("\nFor more information:")
    print("  - README.md - Full documentation")
    print("  - QUICKSTART.md - Quick start guide")
    print("  - TESTING.md - Testing guide")
    print("\n" + "="*50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())