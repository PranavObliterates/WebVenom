# WebVenom Reference Demos

This directory contains intentionally vulnerable demonstration applications used for testing and validating WebVenom's scanning capabilities.

> **Warning:** These demo applications contain real, exploitable security vulnerabilities (SQL injection, XSS, SSRF, command injection, path traversal, etc.). **Do not deploy these applications to public networks or production environments.**

## Applications

- **`vulnerable-flask/`**: An intentionally vulnerable Flask application with multiple route handlers and SQLite database integration.
- **`vulnerable-django/`**: An intentionally vulnerable Django project with view functions exhibiting various OWASP Top 10 flaws.

## Scanning the Demos

Scan the Flask demo with WebVenom:
```bash
webvenom scan demos/vulnerable-flask/app.py --html flask_report.html
```

Scan the Django demo with WebVenom:
```bash
webvenom scan demos/vulnerable-django/ --html django_report.html
```

## How SQL Injection Works in WebVenom

- **Scanner Detection (SAST)**: WebVenom detects SQL injection via static AST taint analysis (tracing request parameters directly into raw query strings). It analyzes the source code structure, meaning **it never requires a live database connection or pre-existing `.sqlite3` file to detect SQL vulnerabilities**.
- **Live Interactive Demonstrations**: If you want to start the Flask demo locally in a browser (`python demos/vulnerable-flask/app.py`), it automatically initializes its SQLite schema and seed users (`admin`, `alice`, `bob`) on first run so you can interactively demonstrate SQL injection attacks (e.g. logging in via `' OR '1'='1`).
