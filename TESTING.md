# Testing Guide for PersonaProbe

This document outlines how to run, write, and maintain tests for PersonaProbe.

## Setup

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Code coverage reporting
- `pytest-mock` - Mocking support
- `requests-mock` - Mock HTTP requests
- `coverage` - Coverage analysis

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=personaprobe --cov-report=html
```

This generates an HTML report in `htmlcov/index.html`

### Run Specific Test File
```bash
pytest test_personaprobe.py
```

### Run Specific Test Class
```bash
pytest test_personaprobe.py::TestHelperFunctions
```

### Run Specific Test Function
```bash
pytest test_personaprobe.py::TestHelperFunctions::test_print_banner
```

### Run Tests Matching a Pattern
```bash
pytest -k "email"
```

## Test Structure

Tests are organized into classes by functionality:

- **TestHelperFunctions** - Tests for utility functions (banner, headers, requests)
- **TestWebPresence** - Tests for web presence checking
- **TestWhoisInfo** - Tests for WHOIS lookups
- **TestEmailSearch** - Tests for email discovery
- **TestSocialMediaSearch** - Tests for social media profile discovery
- **TestHaveIBeenPwned** - Tests for data breach checking
- **TestMainLogic** - Tests for main application flow

## Key Testing Techniques Used

### 1. Mocking External Requests
```python
def test_check_web_presence_found(self, requests_mock):
    requests_mock.head("http://example.com", status_code=200)
    personaprobe.check_web_presence("example.com")
```

### 2. Capturing Output
```python
def test_print_banner(self, capsys):
    personaprobe.print_banner()
    captured = capsys.readouterr()
    assert "PersonaProbe" in captured.out
```

### 3. Mocking External Libraries
```python
def test_get_whois_info_success(self):
    mock_whois = Mock()
    mock_whois.domain_name = "example.com"
    with patch("personaprobe.whois.whois", return_value=mock_whois):
        personaprobe.get_whois_info("example.com")
```

### 4. Environment Variables
```python
def test_check_hibp_no_api_key(self, monkeypatch):
    monkeypatch.setenv("HIBP_APIKEY", "")
    personaprobe.check_haveibeenpwned("test@example.com")
```

### 5. CLI Argument Testing
```python
def test_main_with_name(self):
    with patch("sys.argv", ["personaprobe.py", "-n", "John Doe"]):
        personaprobe.main()
```

## Coverage Goals

Current test coverage includes:
- ✅ Helper functions (request handling, output)
- ✅ Web presence checking
- ✅ WHOIS information retrieval
- ✅ Email address generation
- ✅ Social media search
- ✅ Data breach checking
- ✅ CLI argument parsing
- ✅ Error handling

Target: **>80% code coverage**

## CI/CD Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- All pull requests

The GitHub Actions workflow (`.github/workflows/tests.yml`) tests against:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

## Writing New Tests

When adding features to PersonaProbe:

1. Write the test first (TDD approach)
2. Ensure it fails initially
3. Implement the feature
4. Verify the test passes
5. Check coverage hasn't decreased

### Test Template
```python
class TestNewFeature:
    """Test description."""

    def test_new_function_basic(self):
        """Test basic functionality."""
        result = personaprobe.new_function("input")
        assert result == "expected_output"

    def test_new_function_error_handling(self):
        """Test error handling."""
        with patch("personaprobe.external_call", side_effect=Exception("Error")):
            result = personaprobe.new_function("input")
            assert result is None  # or expected behavior
```

## Debugging Failed Tests

### Increase Verbosity
```bash
pytest -vv test_personaprobe.py
```

### Show Print Statements
```bash
pytest -s test_personaprobe.py
```

### Drop into Debugger on Failure
```bash
pytest --pdb test_personaprobe.py
```

### Show Local Variables
```bash
pytest --showlocals test_personaprobe.py
```

## Troubleshooting

### ImportError: No module named 'personaprobe'
Ensure you're running tests from the repository root and the main script is named correctly.

### Mocking not working
Ensure you patch at the location where the function is *used*, not where it's defined:
```python
# Correct
with patch("personaprobe.requests.get"):
    ...

# Incorrect
with patch("requests.get"):
    ...
```

### Environment variable not set
Use `monkeypatch` fixture instead of `os.environ`:
```python
def test_with_env(self, monkeypatch):
    monkeypatch.setenv("VAR_NAME", "value")
```

## Best Practices

1. **Isolate tests** - Each test should be independent
2. **Mock external services** - Don't make real API calls
3. **Use descriptive names** - Test names should describe what they test
4. **Test edge cases** - Empty inputs, errors, None values
5. **Keep tests fast** - Aim for <1 second per test
6. **Use fixtures** - Reuse common setup code
7. **One assertion per test** - Or logically related assertions

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- [requests-mock](https://requests-mock.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
