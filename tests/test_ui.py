"""Unit tests for WebVenom Live Web UI."""
import json
import pytest
from webvenom.ui.server import create_ui_app, serialize_scan_result
from security_scanner.models.scan_result import ScanResult
from security_scanner.models.finding import Finding, Severity, VulnerabilityType


@pytest.fixture
def client():
    app = create_ui_app(default_target="examples/safe_flask_app.py")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ui_index_page(client):
    """GET / should serve the HTML5 dashboard with the canvas attack graph."""
    res = client.get("/")
    assert res.status_code == 200
    assert b"WebVenom" in res.data
    assert b"attackGraphCanvas" in res.data
    assert b"Interactive Attack Graph" in res.data


def test_ui_api_scan_safe_app(client):
    """POST /api/scan should return serialized ScanResult JSON."""
    payload = {
        "target": "examples/safe_flask_app.py",
        "dynamic": False,
        "dependencies": False,
    }
    res = client.post("/api/scan", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    data = res.get_json()
    assert "findings" in data
    assert "routes_scanned" in data
    assert "critical_count" in data
    assert data["app_name"] is not None


def test_ui_api_scan_vulnerable_flask(client):
    """POST /api/scan should detect findings on the vulnerable Flask app."""
    payload = {
        "target": "demos/vulnerable-flask/app.py",
        "dynamic": True,
        "dependencies": False,
    }
    res = client.post("/api/scan", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    data = res.get_json()
    assert data["critical_count"] > 0
    types = [f["vuln_type"] for f in data["findings"]]
    assert "SQL_INJECTION" in types


def test_ui_api_scan_invalid_target(client):
    """POST /api/scan with non-existent target should return 400 error."""
    payload = {"target": "non_existent_file_xyz_123.py"}
    res = client.post("/api/scan", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data


def test_ui_api_export_formats(client):
    """GET /api/export/<format> should return downloadable report formats."""
    # Run scan first to cache result
    client.post("/api/scan", data=json.dumps({"target": "examples/safe_flask_app.py"}), content_type="application/json")

    # Export HTML
    res_html = client.get("/api/export/html")
    assert res_html.status_code == 200
    assert b"<!DOCTYPE html>" in res_html.data

    # Export JSON
    res_json = client.get("/api/export/json")
    assert res_json.status_code == 200
    assert res_json.is_json

    # Export SARIF
    res_sarif = client.get("/api/export/sarif")
    assert res_sarif.status_code == 200
    sarif_data = res_sarif.get_json()
    assert sarif_data["version"] == "2.1.0"
