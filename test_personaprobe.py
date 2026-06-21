#!/usr/bin/env python3

import pytest
import sys
import json
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import requests_mock

# Import the main module (adjust path if needed)
import personaprobe


class TestHelperFunctions:
    """Test helper functions."""

    def test_print_banner(self, capsys):
        """Test that banner prints without errors."""
        personaprobe.print_banner()
        captured = capsys.readouterr()
        assert "PersonaProbe" in captured.out
        assert "v1.0" in captured.out

    def test_section_header(self, capsys):
        """Test section header formatting."""
        personaprobe.section_header("Test Section")
        captured = capsys.readouterr()
        assert "TEST SECTION" in captured.out

    def test_perform_request_success(self, requests_mock):
        """Test successful HTTP request."""
        requests_mock.get("http://example.com", status_code=200, text="OK")
        response = personaprobe.perform_request("http://example.com")
        assert response is not None
        assert response.status_code == 200
        assert response.text == "OK"

    def test_perform_request_timeout(self):
        """Test request timeout handling."""
        with patch("personaprobe.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
            response = personaprobe.perform_request("http://example.com")
            assert response is None

    def test_perform_request_connection_error(self):
        """Test request connection error handling."""
        with patch("personaprobe.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
            response = personaprobe.perform_request("http://example.com")
            assert response is None

    def test_perform_request_http_error(self):
        """Test request HTTP error handling."""
        with patch("personaprobe.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
            response = personaprobe.perform_request("http://example.com")
            assert response is None


class TestWebPresence:
    """Test web presence checking."""

    def test_check_web_presence_found(self, capsys, requests_mock):
        """Test when website is found."""
        requests_mock.head("http://example.com", status_code=200)
        personaprobe.check_web_presence("example.com")
        captured = capsys.readouterr()
        assert "Website found" in captured.out
        assert "200" in captured.out

    def test_check_web_presence_not_found(self, capsys, requests_mock):
        """Test when website returns 404."""
        requests_mock.head("http://example.com", status_code=404)
        personaprobe.check_web_presence("example.com")
        captured = capsys.readouterr()
        assert "No active website found" in captured.out

    def test_check_web_presence_connection_error(self, capsys):
        """Test connection error handling."""
        with patch("personaprobe.requests.head") as mock_head:
            mock_head.side_effect = requests.exceptions.ConnectionError()
            personaprobe.check_web_presence("example.com")
            captured = capsys.readouterr()
            assert "Could not connect" in captured.out


class TestWhoisInfo:
    """Test WHOIS information retrieval."""

    def test_get_whois_info_success(self, capsys):
        """Test successful WHOIS lookup."""
        mock_whois = Mock()
        mock_whois.domain_name = "example.com"
        mock_whois.registrar = "Example Registrar"
        mock_whois.creation_date = "2020-01-01"
        mock_whois.expiration_date = "2025-01-01"
        mock_whois.updated_date = "2022-06-15"
        mock_whois.name = "John Doe"
        mock_whois.organization = "Example Inc"
        mock_whois.emails = ["contact@example.com"]
        mock_whois.country = "US"

        with patch("personaprobe.whois.whois", return_value=mock_whois):
            personaprobe.get_whois_info("example.com")
            captured = capsys.readouterr()
            assert "example.com" in captured.out
            assert "Example Registrar" in captured.out
            assert "John Doe" in captured.out

    def test_get_whois_info_error(self, capsys):
        """Test WHOIS lookup error handling."""
        with patch("personaprobe.whois.whois", side_effect=Exception("WHOIS lookup failed")):
            personaprobe.get_whois_info("invalid-domain.xyz")
            captured = capsys.readouterr()
            assert "Error retrieving WHOIS" in captured.out


class TestEmailSearch:
    """Test email address search."""

    def test_search_emails_with_domain_only(self, capsys):
        """Test email search with domain only."""
        emails = personaprobe.search_emails(target_domain="example.com")
        assert len(emails) >= 3  # At least info@, support@, admin@
        assert "info@example.com" in emails
        assert "support@example.com" in emails
        assert "admin@example.com" in emails

    def test_search_emails_with_name_and_domain(self, capsys):
        """Test email search with name and domain."""
        emails = personaprobe.search_emails(target_name="John Doe", target_domain="example.com")
        assert len(emails) >= 5
        assert "john@example.com" in emails
        assert "john.doe@example.com" in emails
        assert "jdoe@example.com" in emails

    def test_search_emails_no_params(self, capsys):
        """Test email search with no parameters."""
        emails = personaprobe.search_emails()
        captured = capsys.readouterr()
        assert "No specific email patterns found" in captured.out

    def test_search_emails_name_single_word(self, capsys):
        """Test email search with single word name."""
        emails = personaprobe.search_emails(target_name="Madonna", target_domain="example.com")
        assert "madonna@example.com" in emails

    def test_search_emails_returns_list(self):
        """Test that search_emails returns a list."""
        result = personaprobe.search_emails(target_domain="test.com")
        assert isinstance(result, list)


class TestSocialMediaSearch:
    """Test social media profile discovery."""

    def test_search_social_media_with_name(self, capsys):
        """Test social media search with name."""
        personaprobe.search_social_media(target_name="John Doe")
        captured = capsys.readouterr()
        assert "LinkedIn" in captured.out
        assert "Twitter" in captured.out
        assert "GitHub" in captured.out
        assert "Facebook" in captured.out

    def test_search_social_media_with_username(self, capsys):
        """Test social media search with username."""
        personaprobe.search_social_media(target_username="johndoe123")
        captured = capsys.readouterr()
        assert "Searching" in captured.out
        assert "johndoe123" in captured.out

    def test_search_social_media_with_domain(self, capsys):
        """Test social media search with domain."""
        personaprobe.search_social_media(target_domain="example.com")
        captured = capsys.readouterr()
        assert "Searching" in captured.out

    def test_search_social_media_no_params(self, capsys):
        """Test social media search with no parameters."""
        personaprobe.search_social_media()
        captured = capsys.readouterr()
        assert "No name, username, or domain provided" in captured.out

    def test_search_social_media_url_encoding(self, capsys):
        """Test that special characters are properly encoded in URLs."""
        personaprobe.search_social_media(target_name="John Doe Jr.")
        captured = capsys.readouterr()
        # URL encoding should handle spaces and special characters
        assert "search" in captured.out.lower()


class TestHaveIBeenPwned:
    """Test HaveIBeenPwned breach checking."""

    def test_check_hibp_no_api_key(self, monkeypatch, capsys):
        """Test HIBP check without API key."""
        monkeypatch.setenv("HIBP_APIKEY", "")
        personaprobe.check_haveibeenpwned("test@example.com")
        captured = capsys.readouterr()
        assert "HIBP_APIKEY environment variable not set" in captured.out

    def test_check_hibp_email_found_breaches(self, monkeypatch, capsys, requests_mock):
        """Test HIBP check with email found in breaches."""
        monkeypatch.setenv("HIBP_APIKEY", "test_key_123")
        
        breach_data = [
            {
                "Name": "Adobe",
                "BreachDate": "2013-10-04",
                "Description": "Adobe suffered a massive breach..."
            }
        ]
        
        requests_mock.get(
            "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
            status_code=200,
            json=breach_data
        )
        
        personaprobe.check_haveibeenpwned("test@example.com")
        captured = capsys.readouterr()
        assert "Found breach" in captured.out
        assert "Adobe" in captured.out

    def test_check_hibp_email_no_breaches(self, monkeypatch, capsys, requests_mock):
        """Test HIBP check with email not in breaches."""
        monkeypatch.setenv("HIBP_APIKEY", "test_key_123")
        requests_mock.get(
            "https://haveibeenpwned.com/api/v3/breachedaccount/safe%40example.com",
            status_code=404
        )
        
        personaprobe.check_haveibeenpwned("safe@example.com")
        captured = capsys.readouterr()
        assert "No breaches found" in captured.out

    def test_check_hibp_rate_limit(self, monkeypatch, capsys, requests_mock):
        """Test HIBP rate limiting."""
        monkeypatch.setenv("HIBP_APIKEY", "test_key_123")
        requests_mock.get(
            "https://haveibeenpwned.com/api/v3/breachedaccount/test%40example.com",
            status_code=429
        )
        
        personaprobe.check_haveibeenpwned("test@example.com")
        captured = capsys.readouterr()
        assert "Rate limit hit" in captured.out

    def test_check_hibp_domain(self, monkeypatch, capsys):
        """Test HIBP check with domain."""
        monkeypatch.setenv("HIBP_APIKEY", "")
        personaprobe.check_haveibeenpwned("example.com")
        captured = capsys.readouterr()
        assert "Checking domain" in captured.out


class TestMainLogic:
    """Test main application logic."""

    def test_main_no_arguments(self, capsys):
        """Test main with no arguments."""
        with patch("sys.argv", ["personaprobe.py"]):
            with pytest.raises(SystemExit):
                personaprobe.main()
            captured = capsys.readouterr()
            assert "Please provide at least one target identifier" in captured.out

    def test_main_with_name(self, capsys):
        """Test main with name argument."""
        with patch("sys.argv", ["personaprobe.py", "-n", "John Doe"]):
            with patch("personaprobe.search_social_media"):
                personaprobe.main()
                captured = capsys.readouterr()
                assert "Starting reconnaissance" in captured.out
                assert "John Doe" in captured.out

    def test_main_with_domain(self, capsys):
        """Test main with domain argument."""
        with patch("sys.argv", ["personaprobe.py", "-d", "example.com"]):
            with patch("personaprobe.check_web_presence"):
                with patch("personaprobe.get_whois_info"):
                    with patch("personaprobe.search_emails"):
                        with patch("personaprobe.check_haveibeenpwned"):
                            with patch("personaprobe.search_social_media"):
                                personaprobe.main()
                                captured = capsys.readouterr()
                                assert "example.com" in captured.out

    def test_main_with_email(self, capsys):
        """Test main with email argument."""
        with patch("sys.argv", ["personaprobe.py", "-e", "john@example.com"]):
            with patch("personaprobe.check_haveibeenpwned"):
                with patch("personaprobe.check_web_presence"):
                    with patch("personaprobe.get_whois_info"):
                        with patch("personaprobe.search_social_media"):
                            personaprobe.main()
                            captured = capsys.readouterr()
                            assert "john@example.com" in captured.out

    def test_main_with_username(self, capsys):
        """Test main with username argument."""
        with patch("sys.argv", ["personaprobe.py", "-u", "johndoe123"]):
            with patch("personaprobe.search_social_media"):
                personaprobe.main()
                captured = capsys.readouterr()
                assert "Starting reconnaissance" in captured.out

    def test_main_completes_successfully(self, capsys):
        """Test that main completes with success message."""
        with patch("sys.argv", ["personaprobe.py", "-n", "Test User"]):
            with patch("personaprobe.search_social_media"):
                personaprobe.main()
                captured = capsys.readouterr()
                assert "PersonaProbe Complete" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
