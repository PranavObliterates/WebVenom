"""Flask-based Local Web UI Server for WebVenom."""
import os
import sys
import logging
import threading
import webbrowser
from typing import Optional
from flask import Flask, request, jsonify, Response, make_response

from .dashboard_html import DASHBOARD_HTML
from ..cli import load_app_from_path
from security_scanner.core.scanner import scan_app
from security_scanner.reporting.html_report import generate_html_report
from security_scanner.reporting.json_report import generate_json_report
from security_scanner.reporting.sarif_report import generate_sarif_report

logger = logging.getLogger(__name__)


def serialize_scan_result(result) -> dict:
    """Serialize ScanResult to a JSON-safe dictionary for the UI."""
    findings = []
    for f in result.findings:
        findings.append({
            "vuln_type": f.vuln_type.value if hasattr(f.vuln_type, "value") else str(f.vuln_type),
            "severity": f.severity.value if hasattr(f.severity, "value") else str(f.severity),
            "endpoint": f.endpoint,
            "file": f.file,
            "line": f.line,
            "code_snippet": f.code_snippet,
            "explanation": f.explanation,
            "fix_recommendation": f.fix_recommendation,
            "fix_before": f.fix_before,
            "fix_after": f.fix_after,
            "reference": f.reference,
            "confidence": f.confidence,
            "source": f.source,
            "status": f.status,
            "rule_id": f.rule_id,
            "cwe": f.cwe,
            "owasp_category": f.vuln_type.owasp_category if hasattr(f.vuln_type, "owasp_category") else "OWASP Top 10",
        })

    return {
        "app_name": result.app_name,
        "routes_scanned": result.routes_scanned,
        "routes_tested": result.routes_tested,
        "scan_duration_seconds": result.scan_duration_seconds,
        "critical_count": result.critical_count,
        "high_count": result.high_count,
        "medium_count": result.medium_count,
        "low_count": result.low_count,
        "warnings": result.warnings,
        "findings": findings,
    }


def create_ui_app(default_target: str = "") -> Flask:
    """Create and configure the WebVenom UI Flask application."""
    app = Flask("webvenom_ui")
    app.config["JSON_SORT_KEYS"] = False
    last_scan_cache = {"result": None, "target": default_target}

    @app.route("/", methods=["GET"])
    def index():
        html = DASHBOARD_HTML
        if default_target:
            html = html.replace('value="demos/vulnerable-flask/app.py"', f'value="{default_target}"')
        return Response(html, mimetype="text/html")

    @app.route("/api/scan", methods=["POST"])
    def api_scan():
        data = request.get_json(silent=True) or {}
        target = data.get("target", "").strip() or default_target or "demos/vulnerable-flask/app.py"
        dynamic = bool(data.get("dynamic", True))
        deps = bool(data.get("dependencies", True))
        osv = bool(data.get("osv", False))

        try:
            target_app = load_app_from_path(target)
            dep_root = (
                os.path.abspath(target) if deps and os.path.isdir(target)
                else os.path.dirname(os.path.abspath(target)) if deps
                else ""
            )
            result = scan_app(
                target_app,
                dynamic=dynamic,
                dependency_root=dep_root,
                osv_lookup=osv
            )
            last_scan_cache["result"] = result
            last_scan_cache["target"] = target
            return jsonify(serialize_scan_result(result))
        except Exception as exc:
            logger.exception("Web UI Scan failed")
            return jsonify({"error": str(exc)}), 400

    @app.route("/api/export/<format_type>", methods=["GET"])
    def api_export(format_type: str):
        result = last_scan_cache.get("result")
        target = request.args.get("target") or last_scan_cache.get("target") or "demos/vulnerable-flask/app.py"

        if result is None:
            try:
                target_app = load_app_from_path(target)
                result = scan_app(target_app, dynamic=True)
                last_scan_cache["result"] = result
            except Exception as exc:
                return f"Error scanning target for export: {exc}", 400

        fmt = format_type.lower()
        if fmt == "html":
            content = generate_html_report(result)
            resp = make_response(content)
            resp.headers["Content-Type"] = "text/html"
            resp.headers["Content-Disposition"] = f'attachment; filename="{result.app_name}_security_report.html"'
            return resp
        elif fmt == "json":
            content = generate_json_report(result)
            resp = make_response(content)
            resp.headers["Content-Type"] = "application/json"
            resp.headers["Content-Disposition"] = f'attachment; filename="{result.app_name}_security_report.json"'
            return resp
        elif fmt in ("sarif", "github"):
            import json
            sarif_doc = generate_sarif_report(result)
            content = json.dumps(sarif_doc, indent=2)
            resp = make_response(content)
            resp.headers["Content-Type"] = "application/json"
            resp.headers["Content-Disposition"] = f'attachment; filename="{result.app_name}_results.sarif"'
            return resp
        else:
            return f"Unsupported export format '{format_type}'. Supported: html, json, sarif.", 400

    return app


def run_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: bool = True,
    default_target: str = ""
) -> None:
    """Launch the WebVenom UI server and open the browser."""
    app = create_ui_app(default_target=default_target)
    url = f"http://{host}:{port}"
    print(f"\n🕷️  WebVenom Live Security Dashboard running at: {url}")
    print("   Press Ctrl+C to stop the server.\n")

    if open_browser:
        def _open():
            threading.Event().wait(0.7)
            webbrowser.open(url)
        threading.Thread(target=_open, daemon=True).start()

    app.run(host=host, port=port, debug=False)
