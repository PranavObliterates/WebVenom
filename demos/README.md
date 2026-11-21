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
