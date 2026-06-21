#!/usr/bin/env python3

import requests
import sys
import argparse
import logging
import json
import os
import re
from urllib.parse import quote_plus
from datetime import datetime

# Try different whois imports for compatibility
try:
    from whois import whois as whois_lookup
except ImportError:
    try:
        import whois
        whois_lookup = whois.whois
    except (ImportError, AttributeError):
        whois_lookup = None

# Configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HAVEIBEENPWNED_API_KEY = os.environ.get("HIBP_APIKEY")
LOG_FILE = "personaprobe.log"
TIMEOUT = 10

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Validation Functions
def is_valid_email(email):
    """Validate email format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_domain(domain):
    """Validate domain format."""
    if not domain or not isinstance(domain, str):
        return False
    # Basic domain validation
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None


def is_valid_name(name):
    """Validate name format."""
    if not name or not isinstance(name, str):
        return False
    # Name should contain only letters, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z\s'-]{2,}$"
    return re.match(pattern, name) is not None


def is_valid_username(username):
    """Validate username format."""
    if not username or not isinstance(username, str):
        return False
    # Username should be alphanumeric with underscores/hyphens, 3-32 chars
    pattern = r'^[a-zA-Z0-9_-]{3,32}$'
    return re.match(pattern, username) is not None


# Helper Functions
def print_banner():
    """Prints a simple banner."""
    print("""
    ╔═══════════════════════════════╗
    ║     PersonaProbe v1.1         ║
    ║    by Superintellect          ║
    ╚═══════════════════════════════╝
    """)
    print("- Persona Probe: Information Gathering Tool -")
    logger.info("PersonaProbe started")


def perform_request(url, headers=None, params=None, timeout=TIMEOUT):
    """Helper to perform HTTP GET requests with error handling."""
    if not url or not isinstance(url, str):
        logger.error(f"Invalid URL provided: {url}")
        return None
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout,
            allow_redirects=True
        )
        
        # Don't raise on 404 or 429, just return the response
        if response.status_code not in [404, 429]:
            response.raise_for_status()
        
        logger.debug(f"Request to {url} returned status {response.status_code}")
        return response
    
    except requests.exceptions.Timeout:
        logger.error(f"Request to {url} timed out after {timeout}s")
        print(f"[!] Request to {url} timed out", file=sys.stderr)
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error to {url}: {e}")
        print(f"[!] Connection error to {url}: {e}", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from {url}: {e}")
        print(f"[!] HTTP error from {url}: {e}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to {url} failed: {e}")
        print(f"[!] Request to {url} failed: {e}", file=sys.stderr)
        return None
    except Exception as e:
        logger.error(f"Unexpected error during request to {url}: {e}")
        print(f"[!] Unexpected error: {e}", file=sys.stderr)
        return None


def section_header(title):
    """Print a section header."""
    header = f"\n{'='*5} {title.upper()} {'='*5}"
    print(header)
    logger.info(f"Section: {title}")


# Information Gathering Modules
def check_web_presence(target_domain):
    """Checks if a domain has an active website."""
    if not is_valid_domain(target_domain):
        logger.warning(f"Invalid domain format: {target_domain}")
        print(f"[!] Invalid domain format: {target_domain}")
        return
    
    section_header("Web Presence")
    print(f"[+] Checking web presence for: {target_domain}")
    
    try:
        # Try both http and https
        for protocol in ['https', 'http']:
            url = f'{protocol}://{target_domain}'
            try:
                response = requests.head(
                    url,
                    timeout=5,
                    allow_redirects=True,
                    headers={'User-Agent': USER_AGENT}
                )
                
                if response.status_code < 400:
                    print(f"[+] Website found at {url} (Status: {response.status_code})")
                    logger.info(f"Website found at {url} with status {response.status_code}")
                    return
                elif response.status_code < 500:
                    print(f"[!] {url} returned status {response.status_code}")
                    
            except requests.exceptions.RequestException:
                continue
        
        print(f"[-] No active website found for {target_domain}")
        logger.info(f"No active website found for {target_domain}")
        
    except Exception as e:
        logger.error(f"Unexpected error checking web presence for {target_domain}: {e}")
        print(f"[!] Error checking web presence: {e}")


def get_whois_info(target_domain):
    """Retrieves WHOIS information for a domain."""
    if not is_valid_domain(target_domain):
        logger.warning(f"Invalid domain format: {target_domain}")
        print(f"[!] Invalid domain format: {target_domain}")
        return
    
    section_header("WHOIS Information")
    print(f"[+] Querying WHOIS for {target_domain}")
    
    # Check if whois module is available
    if whois_lookup is None:
        logger.warning("WHOIS module not available")
        print("[!] WHOIS module not properly installed")
        print("[*] Install with: pip install python-whois")
        return
    
    try:
        w = whois_lookup(target_domain)
        
        # Safely handle all attributes
        whois_data = {
            'domain_name': getattr(w, 'domain_name', None),
            'registrar': getattr(w, 'registrar', None),
            'creation_date': getattr(w, 'creation_date', None),
            'expiration_date': getattr(w, 'expiration_date', None),
            'updated_date': getattr(w, 'updated_date', None),
            'name': getattr(w, 'name', None),
            'organization': getattr(w, 'organization', None),
            'emails': getattr(w, 'emails', None),
            'country': getattr(w, 'country', None),
        }
        
        # Print available information
        found_info = False
        for key, value in whois_data.items():
            if value:
                found_info = True
                display_key = key.replace('_', ' ').title()
                if isinstance(value, (list, tuple)):
                    value_str = ', '.join(str(v) for v in value if v)
                else:
                    value_str = str(value)
                print(f"[*] {display_key}: {value_str}")
        
        if not found_info:
            print("[-] No WHOIS information found")
            logger.info(f"No WHOIS data available for {target_domain}")
        else:
            logger.info(f"Successfully retrieved WHOIS for {target_domain}")
        
    except Exception as e:
        logger.error(f"Error retrieving WHOIS for {target_domain}: {e}")
        print(f"[!] WHOIS lookup unavailable for {target_domain}")
        print(f"[*] This is normal for some domains (try manual lookup at whois.com)")


def search_emails(target_name=None, target_domain=None):
    """Attempts to find email addresses based on patterns."""
    section_header("Email Address Search")
    found_emails = set()
    
    # Validate inputs
    if target_name and not is_valid_name(target_name):
        logger.warning(f"Invalid name format: {target_name}")
        target_name = None
    
    if target_domain and not is_valid_domain(target_domain):
        logger.warning(f"Invalid domain format: {target_domain}")
        target_domain = None
    
    if not target_domain:
        print("[-] No domain provided for email search")
        logger.info("Email search skipped: no domain provided")
        return list(found_emails)
    
    print(f"[+] Attempting to find emails for domain {target_domain} (via common patterns)")
    
    # Common patterns
    common_patterns = [
        f"info@{target_domain}",
        f"support@{target_domain}",
        f"admin@{target_domain}",
        f"contact@{target_domain}",
        f"hello@{target_domain}",
    ]
    
    # Add name-based patterns
    if target_name:
        try:
            name_parts = target_name.strip().split()
            
            if name_parts:
                first_name = name_parts[0].lower()
                last_name = name_parts[-1].lower() if len(name_parts) > 1 else None
                
                if first_name:
                    common_patterns.append(f"{first_name}@{target_domain}")
                
                if last_name and first_name != last_name:
                    common_patterns.append(f"{first_name}.{last_name}@{target_domain}")
                    common_patterns.append(f"{first_name[0]}{last_name}@{target_domain}")
                    common_patterns.append(f"{last_name}@{target_domain}")
        except Exception as e:
            logger.warning(f"Error processing name for email patterns: {e}")
    
    # Add unique emails to set
    for email in common_patterns:
        if is_valid_email(email):
            found_emails.add(email)
            print(f"[?] Potential email: {email}")
    
    if not found_emails:
        print("[-] No valid email patterns generated")
        logger.info("No valid email patterns generated")
    else:
        logger.info(f"Generated {len(found_emails)} potential emails")
    
    return list(found_emails)


def search_social_media(target_name=None, target_username=None, target_domain=None):
    """Searches for social media profiles."""
    section_header("Social Media Profile Discovery")
    
    search_terms = []
    
    # Validate and add search terms
    if target_name and is_valid_name(target_name):
        search_terms.append(target_name)
    if target_username and is_valid_username(target_username):
        search_terms.append(target_username)
    if target_domain and is_valid_domain(target_domain):
        search_terms.append(target_domain)
    
    if not search_terms:
        print("[-] No valid search terms provided for social media search")
        logger.info("Social media search skipped: no valid search terms")
        return
    
    platforms = {
        "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords={}",
        "Twitter": "https://twitter.com/search?q={}",
        "GitHub": "https://github.com/search?q={}",
        "Facebook": "https://www.facebook.com/public/{}",
        "Reddit": "https://www.reddit.com/search/?q={}",
        "Instagram": "https://www.instagram.com/explore/tags/{}/",
    }
    
    for platform, url_template in platforms.items():
        print(f"[+] Searching {platform}...")
        for term in search_terms:
            try:
                encoded_term = quote_plus(term)
                search_url = url_template.format(encoded_term)
                print(f"[?] Potential {platform} search URL: {search_url}")
                logger.debug(f"Generated {platform} search URL for term: {term}")
            except Exception as e:
                logger.warning(f"Error generating {platform} URL for term {term}: {e}")
    
    print("[*] Manual verification of social media links is required.")
    logger.info("Social media search completed")


def check_haveibeenpwned(email_or_domain):
    """Checks HaveIBeenPwned for breaches."""
    section_header("Public Data Breach Check (HaveIBeenPwned)")
    
    # Validate input
    is_email = "@" in email_or_domain if email_or_domain else False
    
    if is_email and not is_valid_email(email_or_domain):
        logger.warning(f"Invalid email format: {email_or_domain}")
        print(f"[!] Invalid email format: {email_or_domain}")
        return
    
    if not is_email and not is_valid_domain(email_or_domain):
        logger.warning(f"Invalid domain format: {email_or_domain}")
        print(f"[!] Invalid domain format: {email_or_domain}")
        return
    
    if not HAVEIBEENPWNED_API_KEY:
        logger.warning("HIBP API key not set")
        print("[!] HIBP_APIKEY environment variable not set. Limited functionality may occur.")
        print("[*] Get your API key from https://haveibeenpwned.com/API/Key and set it as HIBP_APIKEY")
        print(f"[*] Manual check: https://haveibeenpwned.com/?q={email_or_domain}")
        return
    
    headers = {
        "User-Agent": USER_AGENT,
        "hibp-api-key": HAVEIBEENPWNED_API_KEY,
    }
    
    try:
        if is_email:
            print(f"[+] Checking email {email_or_domain} for breaches...")
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote_plus(email_or_domain)}"
            
            response = perform_request(url, headers=headers)
            
            if response is None:
                logger.error(f"Failed to check HIBP for {email_or_domain}")
                return
            
            if response.status_code == 200:
                try:
                    breaches = response.json()
                    if isinstance(breaches, list):
                        for breach in breaches:
                            name = breach.get('Name', 'Unknown')
                            date = breach.get('BreachDate', 'Unknown')
                            title = breach.get('Title', name)
                            print(f"[!] Found breach: {name} ({date}) - {title}")
                            logger.warning(f"Breach found for {email_or_domain}: {name}")
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON response from HIBP for {email_or_domain}")
                    print("[!] Invalid response from HIBP API")
            
            elif response.status_code == 404:
                print(f"[+] No breaches found for {email_or_domain}")
                logger.info(f"No breaches found for {email_or_domain}")
            
            elif response.status_code == 429:
                logger.warning("HIBP rate limit hit")
                print("[!] Rate limit hit for HIBP API. Please wait and try again.")
            
            else:
                logger.warning(f"HIBP returned status {response.status_code} for {email_or_domain}")
                print(f"[!] Could not check email (Status: {response.status_code})")
        
        else:
            print(f"[+] Checking domain {email_or_domain} for breaches...")
            print(f"[*] Manual check: https://haveibeenpwned.com/?q={email_or_domain}")
            logger.info(f"Domain breach check for {email_or_domain} (requires manual verification)")
    
    except Exception as e:
        logger.error(f"Error checking HIBP for {email_or_domain}: {e}")
        print(f"[!] Error checking HIBP: {e}")


# Main Logic
def main():
    """Main function."""
    try:
        print_banner()
        
        parser = argparse.ArgumentParser(
            description="PersonaProbe: An information gathering tool for people and organizations",
            epilog="Example: personaprobe.py -d example.com -n 'John Doe'"
        )
        parser.add_argument("-n", "--name", help="Target's full name (e.g., 'John Doe')")
        parser.add_argument("-u", "--username", help="Target's common username (e.g., 'johndoe123')")
        parser.add_argument("-d", "--domain", help="Target's domain (e.g., 'example.com')")
        parser.add_argument("-e", "--email", help="Target's email address (e.g., 'john@example.com')")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
        
        args = parser.parse_args()
        
        # Set logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        # Validate at least one argument
        if not (args.name or args.username or args.domain or args.email):
            parser.print_help()
            print("\n[!] Please provide at least one target identifier (name, username, domain, or email).")
            logger.warning("No target identifier provided")
            sys.exit(1)
        
        # Display target information
        print("[+] Starting reconnaissance for:")
        if args.name:
            print(f"    Name: {args.name}")
        if args.username:
            print(f"    Username: {args.username}")
        if args.domain:
            print(f"    Domain: {args.domain}")
        if args.email:
            print(f"    Email: {args.email}")
        
        logger.info(f"Reconnaissance started - Name: {args.name}, Username: {args.username}, Domain: {args.domain}, Email: {args.email}")
        
        # Execute Modules
        if args.domain:
            check_web_presence(args.domain)
            get_whois_info(args.domain)
            search_emails(target_name=args.name, target_domain=args.domain)
            check_haveibeenpwned(args.domain)
        
        if args.email:
            check_haveibeenpwned(args.email)
            
            # If email is provided, try to infer domain
            if not args.domain and "@" in args.email:
                try:
                    inferred_domain = args.email.split("@")[1]
                    if is_valid_domain(inferred_domain):
                        print(f"\n[+] Inferring domain from email: {inferred_domain}")
                        logger.info(f"Inferred domain from email: {inferred_domain}")
                        check_web_presence(inferred_domain)
                        get_whois_info(inferred_domain)
                        check_haveibeenpwned(inferred_domain)
                except Exception as e:
                    logger.error(f"Error inferring domain from email: {e}")
        
        search_social_media(
            target_name=args.name,
            target_username=args.username,
            target_domain=args.domain,
        )
        
        # Completion message
        print("\n" + "="*50)
        print("[+] PersonaProbe Complete")
        print("[*] Remember that manual investigation and correlation of findings are crucial for effective OSINT.")
        print(f"[*] Log file saved to: {LOG_FILE}")
        print("="*50)
        
        logger.info("Reconnaissance completed successfully")
    
    except KeyboardInterrupt:
        print("\n[!] PersonaProbe interrupted by user")
        logger.warning("PersonaProbe interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        print(f"[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
