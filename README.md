# WebVenom — Python Security Scanner (SAST + DAST)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![OWASP Top 10](https://img.shields.io/badge/OWASP-Top%2010%20(2021)-orange.svg)](https://owasp.org/Top10/)

**WebVenom** is an installable security scanner for Python web applications (**Flask, Django, and FastAPI**). It combines deep source code analysis (SAST) with bounded, private-target-only dynamic security checks (DAST).

It generates terminal summaries with ANSI syntax highlighting, machine-readable JSON, OASIS SARIF v2.1.0 output for GitHub Code Scanning, interactive HTML dashboards, and **executive PDF reports with AI-assisted code remediation guidance powered by Google Gemini**.

> WebVenom detects all 10 OWASP Top 10 (2021) vulnerability classes across Python Flask, Django, and FastAPI applications.

The framework scanner provides AST-based taint analysis and passive in-process baseline checks. The optional URL crawler audits localhost/private-network targets with strict page, request, timeout, and rate bounds. Its opt-in active probe is a harmless reflection canary, not an exploit tool.

**Contents:** [OWASP Coverage](#-owasp-top-10-coverage) · [Installation](#-installation) · [Architecture](#-architecture--how-it-works) · [Usage](#-usage) · [AI Remediation](#-optional-ai-remediation-guidance-zero-disk-persistence) · [Remote DAST](#remote-dast) · [Tests](#-running-tests--evaluation) · [Repository Layout](#-repository-layout)

---

## 🛡️ OWASP Top 10 Coverage

| OWASP Category | Vulnerability Type | Detection Method |
|---|---|---|
| **A01: Broken Access Control** | Path Traversal / Arbitrary File Read | SAST (Taint tracking to file system sinks) |
| **A01: Broken Access Control** | Open Redirects | SAST (Source-to-redirect sinks) |
| **A01: Broken Access Control** | Missing CSRF Protection | SAST (Configuration audit) |
| **A02: Cryptographic Failures** | Hardcoded Secrets & API Keys | SAST (AST Pattern Engine & Entropy) |
| **A02: Cryptographic Failures** | Broken Hashing (MD4, MD5, SHA-1, SHA-0) | SAST (Hash function call tracking) |
| **A02: Cryptographic Failures** | Insecure Cookie Attributes (Missing Secure/HttpOnly/SameSite) | DAST (Runtime Headers) |
| **A03: Injection** | SQL Injection (SQLi) | SAST (Source-to-sink AST analysis) |
| **A03: Injection** | Cross-Site Scripting (Reflected XSS) | SAST (Unescaped output flows) |
| **A03: Injection** | Command Injection (RCE) | SAST (Shell execution sinks) |
| **A03: Injection** | Server-Side Template Injection (SSTI) | SAST (Template rendering sinks) |
| **A05: Security Misconfiguration** | Debug Mode Enabled in Production | SAST (Global Configuration) |
| **A05: Security Misconfiguration** | CORS Wildcard with Credentials | SAST (CORS Configuration) |
| **A05: Security Misconfiguration** | Missing Security Headers (CSP, HSTS, X-Frame) | DAST (Response Headers) |
| **A06: Vulnerable & Outdated Components** | Unpinned Dependencies & Known CVEs (OSV.dev) | SAST (Dependency Manifest Audit) |
| **A07: Identification & Authentication Failures** | JWT signature, algorithm, and hardcoded-key misuse | SAST (Token handling analysis) |
| **A08: Software & Data Integrity** | Insecure Deserialization (pickle, PyYAML) | SAST (Deserialization sinks) |
| **A10: Server-Side Request Forgery** | SSRF (Unchecked HTTP requests) | SAST (Outbound request sinks) |

---

## 🚀 Installation

### Install directly from GitHub
```bash
pip install git+https://github.com/PranavObliterates/WebVenom.git
```

### Clone and install locally (development mode)
```bash
git clone https://github.com/PranavObliterates/WebVenom.git
cd WebVenom
pip install -e .
```

For JavaScript-rendered page discovery, install the optional browser extra:
```bash
pip install "git+https://github.com/PranavObliterates/WebVenom.git[browser]"
playwright install chromium
```

---

## 🏗️ Architecture & How It Works

WebVenom operates via a dual-engine analysis pipeline designed for speed and reduced false positives:

```
                      ┌────────────────────────────────────────┐
                      │        Target Flask / Django App       │
                      └──────────────────┬─────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
                 ▼                                               ▼
     ┌───────────────────────┐                       ┌───────────────────────┐
     │   Static (SAST)       │                       │   Dynamic (DAST)      │
     │   AST Taint Engine    │                       │   In-Memory Prober    │
     ├───────────────────────┤                       ├───────────────────────┤
     │ • Route AST traversal │                       │ • Test client harness │
     │ • Input source traces │                       │ • Benign baseline     │
     │ • Taint propagation   │                       │ • Response reflection │
     │ • Config audit        │                       │ • Header/Cookie audit │
     └───────────┬───────────┘                       └───────────┬───────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                             ┌───────────────────────┐
                             │      ScanResult       │
                             │ (Normalized Findings) │
                             └───────────┬───────────┘
                                         │
         ┌───────────────────┬───────────┴───────────┬───────────────────┬───────────────────┐
         ▼                   ▼                       ▼                   ▼                   ▼
 ┌───────────────┐   ┌───────────────┐       ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
 │ Console ANSI  │   │  JSON Report  │       │ SARIF v2.1.0  │   │ HTML Dashboard│   │ PDF Executive │
 │ Output        │   │  (CI/CD)      │       │ (GitHub Code) │   │ (Visual UI)   │   │ + Gemini AI   │
 └───────────────┘   └───────────────┘       └───────────────┘   └───────────────┘   └───────────────┘
```

1. **Static Analysis (SAST)**:
   - **AST Analysis Engine**: Parses Python source code into Abstract Syntax Trees using Python's native `ast` module.
   - Reuses parsed syntax trees for identical route sources and caches source lines, reducing repeated setup work across analyzer rules.
   - **Deep Taint Propagation**: Identifies untrusted user input sources (Flask `request.args`, `request.form`, `request.json`, `request.values`, `request.data`, `request.headers`, `request.query_string`; Django `request.GET`, `request.POST`, `request.body`, `request.COOKIES`, `request.FILES`, `request.META`) and tracks data flow across variable assignments, method transformations (e.g. `.strip()`, `.lower()`), nested collections (dictionaries, lists, tuples), string formatting (`.format()`, `%` formatting, f-strings), and intermediate variables into sensitive sinks.
   - **Dangerous Sink Detection**: Catches raw SQL interpolation, `pickle.loads()` / `pickle.load()`, `os.system()` / `subprocess` shell calls, unvalidated `open()` path traversals, unvalidated HTTP calls (SSRF), unvalidated redirects, and weak cryptographic hashing (`md4`, `md5`, `sha1`, `sha`, `hmac`).
   - **Sanitization & Safety-Aware**: Accurately recognizes type conversions (`int()`, `float()`), HTML escaping (`markupsafe.escape()`, `html.escape()`), path sanitizers (`werkzeug.utils.secure_filename()`), safe URL generators (`url_for()`, `reverse()`), shell quoting (`shlex.quote()`), and safe subprocess invocations with `shell=False`.
   - **Noise Reduction & Third-Party Isolation**: Isolates application-layer view code and excludes third-party framework code located inside `site-packages` or `dist-packages`, eliminating false positives in library internals.
   - **Configuration Auditing**: Inspects Flask and Django application configurations for insecure `DEBUG = True`, weak or hardcoded `SECRET_KEY`, missing `CSRF` protection, and missing security middleware.

2. **Dynamic Analysis (DAST)**:
   - **Passive Baseline Checks**: Uses framework test clients only for benign requests. It never generates or sends destructive or invasive payloads.
   - **Endpoint Risk Identification**: SAST maps untrusted input to dangerous sinks and reports the affected endpoint, source file, line, confidence, and remediation. DAST complements this with response-header, cookie, and baseline error checks.
   - **Transport & Cookie Audit**: Analyzes response headers (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`) and inspects session cookies for `Secure`, `HttpOnly`, and `SameSite` flags.

3. **Reporting & AI Insights**:
   - **Console Output**: Instant ANSI color-coded vulnerability summaries with remediation code diffs (`fix_before` vs. `fix_after`).
   - **JSON Export**: Machine-readable format conforming to automated vulnerability management platforms and CI/CD pipelines.
   - **SARIF v2.1.0 Export**: OASIS standard format consumed directly by GitHub Code Scanning, GitLab SAST, and VS Code.
   - **HTML Dashboard**: Self-contained visual report with interactive severity filtering and OWASP category mapping.
   - **Executive PDF + Gemini AI**: Formatted PDF report with automatic XML-entity escaping for code snippets, combining metrics with optional session-only Google Gemini AI executive analysis and prioritized developer remediation roadmaps.

---

## 💻 Usage

### 1. In-App Python Code
```python
from webvenom import scan_app, save_pdf_report

# Scan your Flask, Django, or FastAPI app
result = scan_app(app, dynamic=True)

# Generate AI-powered PDF report (prompts for session-only Gemini API key)
save_pdf_report(result, "security_report.pdf", prompt_for_key=True)
```

### 2. Command Line Interface (CLI)
```bash
# Scan a Flask application by file or directory (auto-detects app.py)
webvenom scan demos/vulnerable-flask/app.py --html report.html --pdf report.pdf
webvenom scan demos/vulnerable-flask/ --static-only

# Scan a Django project by directory, manage.py, or wsgi module
webvenom scan demos/vulnerable-django/
webvenom scan demos/vulnerable-django/manage.py
webvenom scan demos/vulnerable-django/vuln_django/wsgi.py --pdf django_audit.pdf

# Scan with session-only Gemini API key for remediation guidance
webvenom scan app.py --pdf audit.pdf --api-key YOUR_GEMINI_KEY

# Export SARIF for GitHub Code Scanning / CI
webvenom scan app.py --sarif results.sarif

# Static-only scan (fast mode without running test client)
webvenom scan app.py --static-only --json report.json

# Audit dependency manifests for unpinned requirements
webvenom scan app.py --static-only --dependencies

# Opt-in harmless canary checks through the local framework test client
webvenom scan app.py --active-dast --no-ai-prompt

# Crawl a local development server (localhost/private IP only)
webvenom scan-url http://127.0.0.1:5000/ --max-pages 40 --max-depth 3 --max-requests 100 --delay 0.25 --json dast.json

# Use optional Playwright to discover links rendered by JavaScript
webvenom scan-url http://127.0.0.1:5000/ --browser

# Query OSV.dev for known vulnerabilities in exact-pinned dependency versions
webvenom scan . --static-only --dependencies --osv

# CI/CD Quality Gate: fail only on HIGH or CRITICAL issues
webvenom scan app.py --fail-on HIGH

# Enable detailed scan timings and crawl request diagnostics
webvenom scan app.py --debug
webvenom scan-url http://127.0.0.1:5000/ --debug

# Filter output by minimum severity and ignore specific rules
webvenom scan app.py --severity MEDIUM --ignore DEBUG_MODE,WEAK_CRYPTO
```

### 3. Configuration Files (`pyproject.toml` or `.webvenomrc`)
WebVenom automatically discovers configuration from `pyproject.toml` or `.webvenomrc` in the project root:

**`pyproject.toml`:**
```toml
[tool.webvenom]
severity = "MEDIUM"
fail_on = "HIGH"
ignore = ["DEBUG_MODE"]
```

**`.webvenomrc`:**
```json
{
  "severity": "MEDIUM",
  "fail_on": "HIGH",
  "ignore": ["DEBUG_MODE"]
}
```

*(Legacy `.pysecurerc` and `[tool.pysecure]` configs remain fully supported for backward compatibility).*

---

## 🤖 Optional AI Remediation Guidance (Zero Disk Persistence)

WebVenom can utilize Google's Gemini API to provide deep, grounded remediation guidance tailored to each finding:
- **Per-Finding Code Analysis**: The scanner provides concrete, context-aware remediation code diffs showing exactly how to fix the issue in your codebase.
- **Session-Only Security**: You enter the Gemini API key into the terminal when prompted. It remains **strictly in volatile process memory** and is **never written to disk, config files, or git**.
- When the terminal or process terminates, the key is completely purged.
- If you skip the prompt or do not have an API key, WebVenom automatically falls back to its deterministic rule engine so PDF generation always succeeds.
- The AI prompt explicitly forbids exploit payloads and attack instructions. The scanner remains completely functional without an API key because every finding includes built-in fix recommendations.

---

## Remote DAST

### Safety limits

`scan-url` accepts only `http://` or `https://` localhost/private IP targets; DNS hostnames other than `localhost` are rejected. It blocks cross-origin links and redirects, caps response bodies at 1 MB, and applies a minimum 0.1-second delay plus a hard request budget. Public IP targets are rejected. The crawler discovers HTML links and forms but **does not submit forms**. Active canaries are optional and only add a unique query marker to HTML GET pages. Browser mode applies the same private-origin restriction and request budget.

### Authentication and authorization

Authentication is supplied as a JSON workflow file. Put secret values in environment variables; the file contains only references:

```json
{
  "login": {
    "method": "POST",
    "path": "/login",
    "csrf": {"path": "/login", "field": "csrf_token"},
    "form": {
      "username": {"env": "WEBVENOM_TEST_USERNAME"},
      "password": {"env": "WEBVENOM_TEST_PASSWORD"}
    }
  },
  "authorization": [
    {
      "path": "/admin",
      "unauthenticated_statuses": [302, 401, 403],
      "authenticated_statuses": [200]
    }
  ]
}
```

The optional `csrf` entry fetches a page first and reads the named hidden input field into the login form. Set credentials in the shell or CI secret store, then run:

```bash
webvenom scan-url http://127.0.0.1:5000/ --auth-config dast-auth.json
```

Authorization checks run only for paths explicitly listed in the workflow. The scanner compares the expected anonymous and authenticated status codes; it does not infer a site's authorization policy. Auth sessions and credentials are held only in process memory and are not written to reports.

OSV lookups send package names and exact versions to `api.osv.dev`; use `--osv` only when network access and external package metadata disclosure are acceptable. Browser support is optional. Playwright performs rendered-page discovery and limited DOM HTML-sink canary checks; it is not full browser-based exploit testing.

---

## 🧪 Running Tests & Evaluation

Run the automated test suite from the repository root:
```bash
pytest
```

Optional framework evaluation scripts are also included:
```bash
python -m scripts.evaluate_flask
python -m scripts.evaluate_django
python -m scripts.evaluate_fastapi
```

---

## 📁 Repository Layout

- `webvenom/` — Public CLI package entrypoint (`cli.py`), versioning, and unified library exports.
- `security_scanner/` — Core scanning engine, OWASP A01–A10 AST analyzers, DAST prober, data models, and multi-format report generators.
- `tests/` — Automated test suite covering SAST analyzers, DAST probers, CLI options, and reporting formats.
- `examples/` — Minimal safe and intentionally vulnerable application patterns for testing and reference.
- `demos/vulnerable-flask/` and `demos/vulnerable-django/` — Complete intentionally vulnerable reference applications (run only locally in an isolated sandbox).
- `scripts/` — Accuracy and benchmark evaluation modules across Flask, Django, and FastAPI.

Generated reports, databases, build artifacts, and local secrets are ignored and should not be committed.

---

### GitHub Actions (including scheduled scans)

WebVenom runs one bounded scan per command. Use your CI scheduler for recurring scans; this example runs on pushes and every Monday:

```yaml
name: WebVenom Security Scan
on:
  push:
    branches: [main]
  schedule:
    - cron: "0 3 * * 1"
permissions:
  contents: read
  security-events: write
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install WebVenom
        run: pip install .
      - name: Scan source
        run: webvenom scan . --static-only --dependencies --sarif webvenom.sarif --fail-on HIGH
      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: webvenom.sarif
```

---

## 📦 Project Source

This project lives on GitHub and is distributed directly from source.
Install directly from the repository:

```bash
pip install git+https://github.com/PranavObliterates/WebVenom.git
```
