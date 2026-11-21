# Contributing to WebVenom

Thank you for your interest in contributing to WebVenom! This project aims to provide high-accuracy, zero-noise SAST and DAST analysis for Python web applications.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/PranavObliterates/WebVenom.git
   cd WebVenom
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Linux/macOS:
   source .venv/bin/activate
   ```

3. Install WebVenom in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. (Optional) Install browser support for JavaScript-rendered crawler testing:
   ```bash
   pip install -e ".[browser]"
   playwright install chromium
   ```

## Running Tests

Run the full pytest suite:
```bash
pytest
```

Run specific test modules:
```bash
pytest tests/test_new_owasp.py
pytest tests/test_cli.py
pytest tests/test_scanner.py
```

Run framework benchmark evaluations:
```bash
python -m scripts.evaluate_flask
python -m scripts.evaluate_django
python -m scripts.evaluate_fastapi
```

## Adding a New Analyzer

WebVenom organizes SAST analyzers in `security_scanner/analyzers/` named according to OWASP Top 10 categories (e.g., `a01_path_traversal.py`, `a03_sql_injection.py`):

1. **Inherit from Base Analyzer**: Analyzers traverse the Python Abstract Syntax Tree (AST) using `ast.NodeVisitor`.
2. **Identify Sources and Sinks**: Trace user-controllable input (`request.args`, `request.form`, `request.json`, etc.) to dangerous sinks.
3. **Account for Sanitization**: Recognize valid escaping or typing functions (e.g. `int()`, `html.escape()`, `secure_filename()`) to prevent false positives.
4. **Register Analyzer**: Add your analyzer class to `security_scanner/core/scanner.py`.
5. **Add Comprehensive Tests**: Include both vulnerable and safe code samples in `tests/` verifying that safe patterns are not flagged.

## Submitting Pull Requests

- Keep PRs focused on a single feature, bug fix, or analyzer improvement.
- Ensure all automated tests pass (`pytest`).
- Describe the vulnerability pattern, CWE mapping, and remediation steps in your pull request description.
