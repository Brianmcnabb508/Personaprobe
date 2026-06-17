#!/usr/bin/env python3

import requests
import whois
import sys
import argparse
import time
import json
import os
from urllib.parse import quote_plus

# Configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HAVEIBEENPWNED_API_KEY = os.environ.get("HIBP_APIKEY")

# Get your API key from https://haveibeenpwned.com/API/Key

# Helper Functions
def print_banner():
    """Prints a simple banner."""
    print("""
    ╔═══════════════════════════════╗
    ║     PersonaProbe v1.0         ║
    ║    by Superintellect          ║
    ╚═══════════════════════════════╝
    """)
    print("- Persona Probe: Information Gathering Tool -")


def perform_request(url, headers=None, params=None, timeout=10):
    """Helper to perform HTTP GET requests."""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"[!] Request to {url} failed: {e}", file=sys.stderr)
        return None


def section_header(title):
    """Print a section header."""
    print(f"\n{'='*5} {title.upper()} {'='*5}")


# Information Gathering Modules
def check_web_presence(target_domain):
    """Checks if a domain has an active website."""
    section_header("Web Presence")
    print(f"[+] Checking web presence for: {target_domain}")
    try:
        response = requests.head(f'http://{target_domain}', timeout=5, allow_redirects=True)
        if response.status_code < 400:
            print(f"[+] Website found at http://{target_domain} (Status: {response.status_code})")
        else:
            print(f"[-] No active website found at http://{target_domain} (Status: {response.status_code})")
    except requests.exceptions.RequestException:
        print(f"[!] Could not connect to http://{target_domain}")


def get_whois_info(target_domain):
    """Retrieves WHOIS information for a domain."""
    section_header("WHOIS Information")
    print(f"[+] Querying WHOIS for {target_domain}")
    try:
        w = whois.whois(target_domain)
        if w.domain_name:
            print(f"[*] Domain Name: {w.domain_name}")
        if w.registrar:
            print(f"[*] Registrar: {w.registrar}")
        if w.creation_date:
            print(f"[*] Creation Date: {w.creation_date}")
        if w.expiration_date:
            print(f"[*] Expiration Date: {w.expiration_date}")
        if w.updated_date:
            print(f"[*] Updated Date: {w.updated_date}")
        if w.name:
            print(f"[*] Registrant Name: {w.name}")
        if w.organization:
            print(f"[*] Registrant Organization: {w.organization}")
        if w.emails:
            print(f"[*] Registrant Emails: {', '.join(w.emails)}")
        if w.country:
            print(f"[*] Registrant Country: {w.country}")
    except Exception as e:
        print(f"[!] Error retrieving WHOIS for {target_domain}: {e}")


def search_emails(target_name=None, target_domain=None):
    """Attempts to find email addresses."""
    section_header("Email Address Search")
    found_emails = set()

    if target_domain:
        print(f"[+] Attempting to find emails for domain {target_domain} (via common patterns)")
        common_patterns = [
            f"info@{target_domain}",
            f"support@{target_domain}",
            f"admin@{target_domain}",
        ]

        if target_name:
            name_parts = target_name.split()
            first_name = name_parts[0].lower() if name_parts else ""
            last_name = name_parts[-1].lower() if len(name_parts) > 1 else ""

            if first_name:
                common_patterns.append(f"{first_name}@{target_domain}")
            if last_name and first_name:
                common_patterns.append(f"{first_name}.{last_name}@{target_domain}")
                common_patterns.append(f"{first_name[0]}{last_name}@{target_domain}")
            if last_name:
                common_patterns.append(f"{last_name}@{target_domain}")

        for email in common_patterns:
            found_emails.add(email)
            print(f"[?] Potential email: {email}")

    if not found_emails:
        print("[-] No specific email patterns found or service integration not implemented.")

    return list(found_emails)


def search_social_media(target_name=None, target_username=None, target_domain=None):
    """Searches for social media profiles."""
    section_header("Social Media Profile Discovery")
    search_terms = []

    if target_name:
        search_terms.append(target_name)
    if target_username:
        search_terms.append(target_username)
    if target_domain:
        search_terms.append(target_domain)

    if not search_terms:
        print("[-] No name, username, or domain provided for social media search")
        return

    platforms = {
        "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords={}",
        "Twitter": "https://twitter.com/search?q={}",
        "GitHub": "https://github.com/search?q={}",
        "Facebook": "https://www.facebook.com/public/{}",
    }

    for platform, url_template in platforms.items():
        print(f"[+] Searching {platform}...")
        for term in search_terms:
            encoded_term = quote_plus(term)
            search_url = url_template.format(encoded_term)
            print(f"[?] Potential {platform} search URL: {search_url}")

    print("[*] Manual verification of social media links is required.")


def check_haveibeenpwned(email_or_domain):
    """Checks HaveIBeenPwned for breaches."""
    section_header("Public Data Breach Check (HaveIBeenPwned)")

    if not HAVEIBEENPWNED_API_KEY:
        print("[!] HIBP_APIKEY environment variable not set. Limited functionality or rate-limiting may occur.")
        print("[*] Get your API key from https://haveibeenpwned.com/API/Key and set it as HIBP_APIKEY")
        print(f"[*] Manual check for {email_or_domain}: https://haveibeenpwned.com/PwnedWebsites#{email_or_domain}")
        return

    headers = {
        "User-Agent": USER_AGENT,
        "hibp-api-key": HAVEIBEENPWNED_API_KEY,
    }

    # Check for breaches by email
    if "@" in email_or_domain:
        print(f"[+] Checking email {email_or_domain} for breaches...")
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote_plus(email_or_domain)}"
        response = perform_request(url, headers=headers)

        if response and response.status_code == 200:
            breaches = response.json()
            for breach in breaches:
                print(f"[!] Found breach: {breach.get('Name')} ({breach.get('BreachDate')}) - {breach.get('Description')}")
        elif response and response.status_code == 404:
            print(f"[+] No breaches found for {email_or_domain}")
        elif response and response.status_code == 429:
            print("[!] Rate limit hit for HIBP API. Please wait and try again, or use a valid API key")
        else:
            print(f"[!] Could not check email {email_or_domain} for breaches")
    else:
        print(f"[+] Checking domain {email_or_domain} for breaches...")
        print(f"[*] Manual check for domain {email_or_domain}: https://haveibeenpwned.com/PwnedWebsites#{email_or_domain}")


# Main Logic
def main():
    """Main function."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="PersonaProbe: An information gathering tool for people and organizations"
    )
    parser.add_argument("-n", "--name", help="Target's full name (e.g., 'John Doe')")
    parser.add_argument("-u", "--username", help="Target's common username (e.g., 'johndoe123')")
    parser.add_argument("-d", "--domain", help="Target's domain (e.g., 'example.com')")
    parser.add_argument("-e", "--email", help="Target's email address (e.g., 'john@example.com')")

    args = parser.parse_args()

    if not (args.name or args.username or args.domain or args.email):
        parser.print_help()
        print("[!] Please provide at least one target identifier (name, username, domain, or email).")
        sys.exit(1)

    print("[+] Starting reconnaissance for:")
    if args.name:
        print(f"    Name: {args.name}")
    if args.username:
        print(f"    Username: {args.username}")
    if args.domain:
        print(f"    Domain: {args.domain}")
    if args.email:
        print(f"    Email: {args.email}")

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
            inferred_domain = args.email.split("@")[1]
            print(f"\n[+] Inferring domain from email: {inferred_domain}")
            check_web_presence(inferred_domain)
            get_whois_info(inferred_domain)
            check_haveibeenpwned(inferred_domain)

    search_social_media(
        target_name=args.name,
        target_username=args.username,
        target_domain=args.domain,
    )

    print("\n" + "="*50)
    print("[+] PersonaProbe Complete")
    print("[*] Remember that manual investigation and correlation of findings are crucial for effective OSINT.")
    print("="*50)


if __name__ == "__main__":
    main()
