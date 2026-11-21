"""HTML5 Dashboard Template for WebVenom Live Web UI."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebVenom — Application Security Dashboard</title>
    <style>
        :root {
            --bg-base: #080b11;
            --bg-surface: #0e131f;
            --bg-card: #131a29;
            --bg-card-hover: #192236;
            --border: #1e293b;
            --border-hover: #334155;
            --border-focus: #10b981;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            
            --sev-critical: #f43f5e;
            --sev-critical-bg: rgba(244, 63, 94, 0.12);
            --sev-high: #f97316;
            --sev-high-bg: rgba(249, 115, 22, 0.12);
            --sev-medium: #f59e0b;
            --sev-medium-bg: rgba(245, 158, 11, 0.12);
            --sev-low: #06b6d4;
            --sev-low-bg: rgba(6, 182, 212, 0.12);
            --sev-info: #64748b;
            --sev-info-bg: rgba(100, 116, 139, 0.12);

            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.25);
            --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, Consolas, monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Top Bar */
        header {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            padding: 0.85rem 1.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }

        .logo-symbol {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #059669, #10b981);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            box-shadow: 0 0 15px var(--accent-glow);
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .version-tag {
            font-size: 0.72rem;
            background: var(--border);
            color: var(--text-secondary);
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            font-family: var(--font-mono);
            font-weight: 500;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .export-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 0.45rem 0.85rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .export-btn:hover {
            border-color: var(--border-hover);
            color: var(--text-primary);
            background: var(--bg-card-hover);
        }

        /* Control / Scan Bar */
        .scan-bar {
            background-color: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            padding: 1rem 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .scan-inputs-row {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .target-input-wrapper {
            flex: 1;
            min-width: 320px;
            position: relative;
        }

        .target-input {
            width: 100%;
            background: var(--bg-base);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.65rem 1rem 0.65rem 2.5rem;
            color: var(--text-primary);
            font-family: var(--font-mono);
            font-size: 0.9rem;
            transition: border-color 0.15s ease;
        }

        .target-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }

        .target-input-icon {
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        .scan-btn {
            background: linear-gradient(135deg, #059669, #10b981);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.65rem 1.5rem;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: transform 0.1s ease, box-shadow 0.15s ease;
            box-shadow: 0 2px 10px var(--accent-glow);
        }

        .scan-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
        }

        .scan-btn:active {
            transform: translateY(0);
        }

        .scan-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .presets-row {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            font-size: 0.82rem;
            color: var(--text-secondary);
        }

        .preset-chip {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 0.25rem 0.65rem;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .preset-chip:hover {
            border-color: var(--accent);
            color: var(--text-primary);
        }

        .options-group {
            display: flex;
            align-items: center;
            gap: 1.25rem;
            margin-left: auto;
        }

        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            cursor: pointer;
            font-size: 0.84rem;
            color: var(--text-secondary);
            user-select: none;
        }

        .checkbox-label input {
            accent-color: var(--accent);
        }

        /* Metrics Bar */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            padding: 1.25rem 1.75rem;
        }

        .metric-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--border);
        }

        .metric-card.critical::before { background: var(--sev-critical); }
        .metric-card.high::before { background: var(--sev-high); }
        .metric-card.medium::before { background: var(--sev-medium); }
        .metric-card.accent::before { background: var(--accent); }

        .metric-title {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
        }

        .metric-value {
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .metric-sub {
            font-size: 0.76rem;
            color: var(--text-secondary);
        }

        /* Main Workspace & Tabs */
        .workspace {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 0 1.75rem 1.75rem 1.75rem;
            gap: 1rem;
        }

        .nav-tabs {
            display: flex;
            border-bottom: 1px solid var(--border);
            gap: 1.5rem;
        }

        .nav-tab {
            background: none;
            border: none;
            border-bottom: 2px solid transparent;
            color: var(--text-secondary);
            font-size: 0.92rem;
            font-weight: 600;
            padding: 0.75rem 0.25rem;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-tab:hover {
            color: var(--text-primary);
        }

        .nav-tab.active {
            color: var(--accent);
            border-bottom-color: var(--accent);
        }

        .tab-panel {
            display: none;
            flex: 1;
        }

        .tab-panel.active {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        /* Attack Graph Panel */
        .graph-container {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            height: 560px;
            position: relative;
            overflow: hidden;
        }

        #attackGraphCanvas {
            width: 100%;
            height: 100%;
            display: block;
            cursor: grab;
        }

        #attackGraphCanvas:active {
            cursor: grabbing;
        }

        .graph-controls {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            display: flex;
            gap: 0.4rem;
            background: rgba(14, 19, 31, 0.85);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.35rem;
            z-index: 10;
        }

        .graph-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: bold;
            transition: all 0.15s ease;
        }

        .graph-btn:hover {
            background: var(--bg-card-hover);
            color: var(--text-primary);
            border-color: var(--border-hover);
        }

        .graph-legend {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(14, 19, 31, 0.85);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.65rem 0.85rem;
            font-size: 0.78rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            z-index: 10;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
        }

        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        /* Findings Matrix View */
        .findings-toolbar {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-box {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.5rem 0.85rem 0.5rem 2.25rem;
            color: var(--text-primary);
            font-size: 0.85rem;
            width: 280px;
            position: relative;
        }

        .search-box-wrapper {
            position: relative;
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .filter-tabs {
            display: flex;
            gap: 0.35rem;
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.25rem;
        }

        .filter-chip {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 0.8rem;
            padding: 0.3rem 0.65rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .filter-chip.active {
            background: var(--bg-card);
            color: var(--text-primary);
            font-weight: 600;
        }

        .findings-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .finding-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
            overflow: hidden;
        }

        .finding-card:hover {
            border-color: var(--border-hover);
            background: var(--bg-card);
        }

        .finding-card.active {
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
        }

        .finding-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.4rem;
        }

        .sev-badge {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .sev-badge.CRITICAL { background: var(--sev-critical-bg); color: var(--sev-critical); border: 1px solid rgba(244, 63, 94, 0.3); }
        .sev-badge.HIGH { background: var(--sev-high-bg); color: var(--sev-high); border: 1px solid rgba(249, 115, 22, 0.3); }
        .sev-badge.MEDIUM { background: var(--sev-medium-bg); color: var(--sev-medium); border: 1px solid rgba(245, 158, 11, 0.3); }
        .sev-badge.LOW { background: var(--sev-low-bg); color: var(--sev-low); border: 1px solid rgba(6, 182, 212, 0.3); }
        .sev-badge.INFO { background: var(--sev-info-bg); color: var(--sev-info); border: 1px solid rgba(100, 116, 139, 0.3); }

        .finding-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .finding-endpoint {
            margin-left: auto;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-muted);
            background: var(--bg-base);
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            border: 1px solid var(--border);
        }

        .finding-meta {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 0.6rem;
        }

        .code-snippet {
            background: var(--bg-base);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.65rem 0.85rem;
            font-family: var(--font-mono);
            font-size: 0.82rem;
            color: #cbd5e1;
            overflow-x: auto;
            white-space: pre;
        }

        /* Slide-Over Drawer */
        .drawer-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(4, 7, 12, 0.65);
            backdrop-filter: blur(4px);
            z-index: 100;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }

        .drawer-backdrop.open {
            opacity: 1;
            pointer-events: auto;
        }

        .drawer {
            position: fixed;
            top: 0;
            right: 0;
            bottom: 0;
            width: 580px;
            max-width: 90vw;
            background: var(--bg-surface);
            border-left: 1px solid var(--border);
            z-index: 101;
            transform: translateX(100%);
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
        }

        .drawer.open {
            transform: translateX(0);
        }

        .drawer-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .drawer-close {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .drawer-body {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .drawer-section-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            font-weight: 700;
        }

        .diff-container {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .diff-block {
            border-radius: 6px;
            padding: 0.65rem 0.85rem;
            font-family: var(--font-mono);
            font-size: 0.82rem;
            border: 1px solid transparent;
        }

        .diff-block.before {
            background: rgba(244, 63, 94, 0.08);
            border-color: rgba(244, 63, 94, 0.25);
            color: #fecdd3;
        }

        .diff-block.after {
            background: rgba(16, 185, 129, 0.08);
            border-color: rgba(16, 185, 129, 0.25);
            color: #a7f3d0;
        }

        /* OWASP Category Coverage Panel */
        .owasp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }

        .owasp-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .owasp-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .owasp-code {
            font-size: 0.82rem;
            font-family: var(--font-mono);
            color: var(--accent);
            font-weight: 700;
        }

        .owasp-name {
            font-size: 0.95rem;
            font-weight: 600;
        }

        .owasp-bar-track {
            height: 6px;
            background: var(--border);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 0.25rem;
        }

        .owasp-bar-fill {
            height: 100%;
            background: var(--accent);
            border-radius: 3px;
            transition: width 0.3s ease;
        }

        /* Loading Overlay */
        .scanner-loader {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(8, 11, 17, 0.7);
            backdrop-filter: blur(5px);
            z-index: 200;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }

        .scanner-loader.active {
            display: flex;
        }

        .pulse-spinner {
            width: 48px;
            height: 48px;
            border: 3px solid rgba(16, 185, 129, 0.15);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand-container">
            <div class="logo-symbol">🐍</div>
            <div class="brand-title">
                WebVenom
                <span class="version-tag">v0.3.0</span>
            </div>
        </div>
        <div class="header-actions">
            <button class="export-btn" onclick="exportReport('html')">📄 Export HTML</button>
            <button class="export-btn" onclick="exportReport('json')">📦 Export JSON</button>
            <button class="export-btn" onclick="exportReport('sarif')">🛡️ Export SARIF</button>
        </div>
    </header>

    <div class="scan-bar">
        <div class="scan-inputs-row">
            <div class="target-input-wrapper">
                <span class="target-input-icon">📂</span>
                <input type="text" id="targetInput" class="target-input" placeholder="e.g. demos/vulnerable-flask/app.py or package:app" value="demos/vulnerable-flask/app.py">
            </div>
            <div class="options-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="dastCheck" checked>
                    <span>DAST Probes</span>
                </label>
                <label class="checkbox-label">
                    <input type="checkbox" id="depsCheck" checked>
                    <span>Dependencies</span>
                </label>
            </div>
            <button class="scan-btn" id="startScanBtn" onclick="runScan()">
                <span>⚡ Execute Audit</span>
            </button>
        </div>
        <div class="presets-row">
            <span>Quick Presets:</span>
            <button class="preset-chip" onclick="setPreset('demos/vulnerable-flask/app.py')">Flask Demo (SQLi/XSS/SSTI/Pickle)</button>
            <button class="preset-chip" onclick="setPreset('demos/vulnerable-django/')">Django Demo (Auth/CSRF/SQLi)</button>
            <button class="preset-chip" onclick="setPreset('examples/safe_flask_app.py')">Safe Flask App (Baseline Clean)</button>
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card accent">
            <span class="metric-title">Total Findings</span>
            <span class="metric-value" id="metricTotal">0</span>
            <span class="metric-sub" id="metricStatus">Ready to scan</span>
        </div>
        <div class="metric-card critical">
            <span class="metric-title">Critical Severity</span>
            <span class="metric-value" id="metricCritical" style="color: var(--sev-critical);">0</span>
            <span class="metric-sub">Immediate exploit risk</span>
        </div>
        <div class="metric-card high">
            <span class="metric-title">High Severity</span>
            <span class="metric-value" id="metricHigh" style="color: var(--sev-high);">0</span>
            <span class="metric-sub">Privilege / Data impact</span>
        </div>
        <div class="metric-card medium">
            <span class="metric-title">Medium / Low</span>
            <span class="metric-value" id="metricMedium">0</span>
            <span class="metric-sub">Misconfig & Hardening</span>
        </div>
        <div class="metric-card">
            <span class="metric-title">Scan Duration</span>
            <span class="metric-value" id="metricTime">0.00s</span>
            <span class="metric-sub" id="metricRoutes">0 routes inspected</span>
        </div>
    </div>

    <div class="workspace">
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="switchTab('graph')">🕸️ Interactive Attack Graph</button>
            <button class="nav-tab" onclick="switchTab('findings')">📋 Findings Matrix</button>
            <button class="nav-tab" onclick="switchTab('owasp')">🛡️ OWASP Top 10 Coverage</button>
        </div>

        <!-- Tab 1: Attack Graph -->
        <div id="tab-graph" class="tab-panel active">
            <div class="graph-container">
                <canvas id="attackGraphCanvas"></canvas>
                <div class="graph-controls">
                    <button class="graph-btn" onclick="zoomGraph(1.2)" title="Zoom In">+</button>
                    <button class="graph-btn" onclick="zoomGraph(0.8)" title="Zoom Out">-</button>
                    <button class="graph-btn" onclick="resetGraphView()" title="Fit View">⛶</button>
                    <button class="graph-btn" onclick="togglePhysics()" id="btnPhysics" title="Pause Physics">⏸</button>
                </div>
                <div class="graph-legend">
                    <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> Target Application</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#94a3b8;"></span> Discovered Route</div>
                    <div class="legend-item"><span class="legend-dot" style="background:var(--sev-critical);"></span> Critical Vulnerability</div>
                    <div class="legend-item"><span class="legend-dot" style="background:var(--sev-high);"></span> High Vulnerability</div>
                    <div class="legend-item"><span class="legend-dot" style="background:var(--sev-medium);"></span> Medium Vulnerability</div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Findings Matrix -->
        <div id="tab-findings" class="tab-panel">
            <div class="findings-toolbar">
                <div class="search-box-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchFilter" class="search-box" placeholder="Filter by endpoint, rule, or CWE..." oninput="filterFindings()">
                </div>
                <div class="filter-tabs">
                    <button class="filter-chip active" onclick="setSeverityFilter('ALL')">All</button>
                    <button class="filter-chip" onclick="setSeverityFilter('CRITICAL')">Critical</button>
                    <button class="filter-chip" onclick="setSeverityFilter('HIGH')">High</button>
                    <button class="filter-chip" onclick="setSeverityFilter('MEDIUM')">Medium</button>
                    <button class="filter-chip" onclick="setSeverityFilter('LOW')">Low</button>
                </div>
            </div>
            <div class="findings-list" id="findingsList"></div>
        </div>

        <!-- Tab 3: OWASP Coverage -->
        <div id="tab-owasp" class="tab-panel">
            <div class="owasp-grid" id="owaspGrid"></div>
        </div>
    </div>

    <!-- Slide-Over Inspector Drawer -->
    <div class="drawer-backdrop" id="drawerBackdrop" onclick="closeDrawer()"></div>
    <div class="drawer" id="findingDrawer">
        <div class="drawer-header">
            <div style="display: flex; align-items: center; gap: 0.65rem;">
                <span class="sev-badge" id="drawerSevBadge">CRITICAL</span>
                <span id="drawerFindingType" style="font-weight: 700; font-size: 1rem;">SQL_INJECTION</span>
            </div>
            <button class="drawer-close" onclick="closeDrawer()">✕</button>
        </div>
        <div class="drawer-body">
            <div>
                <div class="drawer-section-title">Location & Endpoint</div>
                <div style="font-family: var(--font-mono); font-size: 0.88rem; color: var(--text-primary);" id="drawerEndpoint">/login</div>
                <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;" id="drawerFile">app.py:37</div>
            </div>
            <div>
                <div class="drawer-section-title">OWASP Category & CWE</div>
                <div style="font-size: 0.88rem; color: var(--text-secondary);" id="drawerOwasp">A03:2021 - Injection</div>
            </div>
            <div>
                <div class="drawer-section-title">Vulnerable Code Snippet</div>
                <div class="code-snippet" id="drawerSnippet">query = f"SELECT * FROM users WHERE..."</div>
            </div>
            <div>
                <div class="drawer-section-title">Vulnerability Analysis</div>
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;" id="drawerWhy">Variable interpolated into raw query string...</p>
            </div>
            <div>
                <div class="drawer-section-title">Remediation Guide</div>
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 0.75rem;" id="drawerFix">Use parameterized queries.</p>
                <div class="diff-container" id="drawerDiff"></div>
            </div>
        </div>
    </div>

    <!-- Scanner Loader -->
    <div class="scanner-loader" id="scannerLoader">
        <div class="pulse-spinner"></div>
        <div style="font-size: 0.95rem; font-weight: 600; color: var(--text-primary);" id="loaderStatus">Running SAST AST Taint Analysis...</div>
    </div>

    <script>
        let currentScanResult = null;
        let selectedSeverityFilter = 'ALL';
        let graphSimulation = null;
        let graphNodes = [];
        let graphLinks = [];
        let graphScale = 1;
        let graphPan = { x: 0, y: 0 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let draggedNode = null;
        let physicsEnabled = true;

        // Initialize on Load
        window.addEventListener('DOMContentLoaded', () => {
            initCanvas();
            runScan(); // Auto-scan initial target
        });

        function setPreset(path) {
            document.getElementById('targetInput').value = path;
            runScan();
        }

        async function runScan() {
            const target = document.getElementById('targetInput').value.trim();
            if (!target) return;

            const loader = document.getElementById('scannerLoader');
            const scanBtn = document.getElementById('startScanBtn');
            loader.classList.add('active');
            scanBtn.disabled = true;

            const payload = {
                target: target,
                dynamic: document.getElementById('dastCheck').checked,
                dependencies: document.getElementById('depsCheck').checked
            };

            try {
                const res = await fetch('/api/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.error) {
                    alert('Scan Error: ' + data.error);
                } else {
                    currentScanResult = data;
                    renderResults(data);
                }
            } catch (err) {
                console.error(err);
                alert('Scan failed: ' + err.message);
            } finally {
                loader.classList.remove('active');
                scanBtn.disabled = false;
            }
        }

        function renderResults(data) {
            // Update Metrics
            document.getElementById('metricTotal').textContent = data.findings.length;
            document.getElementById('metricCritical').textContent = data.critical_count;
            document.getElementById('metricHigh').textContent = data.high_count;
            document.getElementById('metricMedium').textContent = data.medium_count + data.low_count;
            document.getElementById('metricTime').textContent = data.scan_duration_seconds.toFixed(3) + 's';
            document.getElementById('metricRoutes').textContent = `${data.routes_scanned} routes discovered (${data.routes_tested} tested)`;
            document.getElementById('metricStatus').textContent = `${data.app_name} scanned`;

            // Build Graph
            buildGraphData(data);

            // Build Findings List
            filterFindings();

            // Build OWASP Breakdown
            renderOwaspGrid(data);
        }

        /* ---------------- Attack Graph Engine ---------------- */
        function initCanvas() {
            const canvas = document.getElementById('attackGraphCanvas');
            const ctx = canvas.getContext('2d');
            
            function resize() {
                canvas.width = canvas.parentElement.clientWidth * window.devicePixelRatio;
                canvas.height = canvas.parentElement.clientHeight * window.devicePixelRatio;
                ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
            }
            window.addEventListener('resize', resize);
            resize();

            // Mouse Interaction
            canvas.addEventListener('mousedown', (e) => {
                const rect = canvas.getBoundingClientRect();
                const mouseX = (e.clientX - rect.left - graphPan.x) / graphScale;
                const mouseY = (e.clientY - rect.top - graphPan.y) / graphScale;

                // Check node hit
                for (let n of graphNodes) {
                    const dist = Math.hypot(n.x - mouseX, n.y - mouseY);
                    if (dist < n.radius + 6) {
                        draggedNode = n;
                        n.fx = n.x;
                        n.fy = n.y;
                        if (n.findingData) {
                            openDrawer(n.findingData);
                        }
                        return;
                    }
                }
                isDragging = true;
                dragStart = { x: e.clientX - graphPan.x, y: e.clientY - graphPan.y };
            });

            window.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                if (draggedNode) {
                    draggedNode.fx = (e.clientX - rect.left - graphPan.x) / graphScale;
                    draggedNode.fy = (e.clientY - rect.top - graphPan.y) / graphScale;
                } else if (isDragging) {
                    graphPan.x = e.clientX - dragStart.x;
                    graphPan.y = e.clientY - dragStart.y;
                }
            });

            window.addEventListener('mouseup', () => {
                if (draggedNode) {
                    draggedNode.fx = null;
                    draggedNode.fy = null;
                    draggedNode = null;
                }
                isDragging = false;
            });

            canvas.addEventListener('wheel', (e) => {
                e.preventDefault();
                const factor = e.deltaY < 0 ? 1.1 : 0.9;
                zoomGraph(factor);
            });

            requestAnimationFrame(renderGraphLoop);
        }

        function buildGraphData(data) {
            graphNodes = [];
            graphLinks = [];
            const canvas = document.getElementById('attackGraphCanvas');
            const w = canvas.parentElement.clientWidth;
            const h = canvas.parentElement.clientHeight;
            graphPan = { x: w / 2, y: h / 2 };
            graphScale = 1;

            // Root Node
            const rootNode = {
                id: 'root',
                label: data.app_name || 'Target App',
                type: 'root',
                radius: 24,
                color: '#10b981',
                x: 0,
                y: 0,
                vx: 0,
                vy: 0
            };
            graphNodes.push(rootNode);

            // Route Nodes
            const routeMap = new Map();
            data.findings.forEach((f) => {
                const ep = f.endpoint || '/';
                if (!routeMap.has(ep)) {
                    const angle = Math.random() * Math.PI * 2;
                    const dist = 120 + Math.random() * 40;
                    const rNode = {
                        id: 'route_' + ep,
                        label: ep,
                        type: 'route',
                        radius: 14,
                        color: '#94a3b8',
                        x: Math.cos(angle) * dist,
                        y: Math.sin(angle) * dist,
                        vx: 0,
                        vy: 0
                    };
                    routeMap.set(ep, rNode);
                    graphNodes.push(rNode);
                    graphLinks.push({ source: rootNode, target: rNode, length: 140 });
                }
            });

            // Finding Nodes
            data.findings.forEach((f, idx) => {
                const ep = f.endpoint || '/';
                const parentRoute = routeMap.get(ep) || rootNode;
                const angle = Math.random() * Math.PI * 2;
                const dist = 70 + Math.random() * 30;
                
                let col = '#06b6d4';
                if (f.severity === 'CRITICAL') col = '#f43f5e';
                else if (f.severity === 'HIGH') col = '#f97316';
                else if (f.severity === 'MEDIUM') col = '#f59e0b';

                const fNode = {
                    id: 'finding_' + idx,
                    label: f.vuln_type,
                    type: 'finding',
                    severity: f.severity,
                    radius: 10,
                    color: col,
                    x: parentRoute.x + Math.cos(angle) * dist,
                    y: parentRoute.y + Math.sin(angle) * dist,
                    vx: 0,
                    vy: 0,
                    findingData: f
                };
                graphNodes.push(fNode);
                graphLinks.push({ source: parentRoute, target: fNode, length: 80 });
            });
        }

        function renderGraphLoop() {
            const canvas = document.getElementById('attackGraphCanvas');
            const ctx = canvas.getContext('2d');
            const w = canvas.parentElement.clientWidth;
            const h = canvas.parentElement.clientHeight;

            ctx.clearRect(0, 0, w, h);
            ctx.save();
            ctx.translate(graphPan.x, graphPan.y);
            ctx.scale(graphScale, graphScale);

            // Simple Physics Simulation
            if (physicsEnabled) {
                // Spring force on links
                for (let l of graphLinks) {
                    const dx = l.target.x - l.source.x;
                    const dy = l.target.y - l.source.y;
                    const dist = Math.hypot(dx, dy) || 1;
                    const diff = (dist - l.length) / dist * 0.05;
                    const fx = dx * diff;
                    const fy = dy * diff;
                    if (!l.source.fx) { l.source.x += fx; l.source.y += fy; }
                    if (!l.target.fx) { l.target.x -= fx; l.target.y -= fy; }
                }

                // Repulsion between nodes
                for (let i = 0; i < graphNodes.length; i++) {
                    for (let j = i + 1; j < graphNodes.length; j++) {
                        const n1 = graphNodes[i];
                        const n2 = graphNodes[j];
                        const dx = n2.x - n1.x;
                        const dy = n2.y - n1.y;
                        const dist = Math.hypot(dx, dy) || 1;
                        if (dist < 180) {
                            const force = (180 - dist) / dist * 0.12;
                            if (!n1.fx) { n1.x -= dx * force; n1.y -= dy * force; }
                            if (!n2.fx) { n2.x += dx * force; n2.y += dy * force; }
                        }
                    }
                }
            }

            // Draw Links
            ctx.lineWidth = 1.5;
            for (let l of graphLinks) {
                ctx.strokeStyle = l.target.type === 'finding' ? 'rgba(255,255,255,0.08)' : 'rgba(16, 185, 129, 0.2)';
                ctx.beginPath();
                ctx.moveTo(l.source.x, l.source.y);
                ctx.lineTo(l.target.x, l.target.y);
                ctx.stroke();
            }

            // Draw Nodes
            for (let n of graphNodes) {
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
                ctx.fillStyle = n.color;
                ctx.shadowColor = n.color;
                ctx.shadowBlur = n.type === 'finding' ? 12 : 20;
                ctx.fill();
                ctx.shadowBlur = 0;

                // Border
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Node Labels
                ctx.fillStyle = '#cbd5e1';
                ctx.font = (n.type === 'root' ? 'bold 12px' : '11px') + " 'JetBrains Mono', monospace";
                ctx.textAlign = 'center';
                ctx.fillText(n.label, n.x, n.y + n.radius + 14);
            }

            ctx.restore();
            requestAnimationFrame(renderGraphLoop);
        }

        function zoomGraph(factor) {
            graphScale *= factor;
            graphScale = Math.max(0.3, Math.min(3.5, graphScale));
        }

        function resetGraphView() {
            const canvas = document.getElementById('attackGraphCanvas');
            graphPan = { x: canvas.parentElement.clientWidth / 2, y: canvas.parentElement.clientHeight / 2 };
            graphScale = 1;
        }

        function togglePhysics() {
            physicsEnabled = !physicsEnabled;
            document.getElementById('btnPhysics').textContent = physicsEnabled ? '⏸' : '▶';
        }

        /* ---------------- Tab Switching ---------------- */
        function switchTab(tabId) {
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        }

        /* ---------------- Findings List & Search ---------------- */
        function setSeverityFilter(sev) {
            selectedSeverityFilter = sev;
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            filterFindings();
        }

        function filterFindings() {
            if (!currentScanResult) return;
            const q = document.getElementById('searchFilter').value.toLowerCase();
            const listEl = document.getElementById('findingsList');
            listEl.innerHTML = '';

            const filtered = currentScanResult.findings.filter(f => {
                const matchesSev = selectedSeverityFilter === 'ALL' || f.severity === selectedSeverityFilter;
                const matchesSearch = !q || 
                    f.vuln_type.toLowerCase().includes(q) || 
                    f.endpoint.toLowerCase().includes(q) ||
                    f.explanation.toLowerCase().includes(q) ||
                    (f.code_snippet && f.code_snippet.toLowerCase().includes(q));
                return matchesSev && matchesSearch;
            });

            if (filtered.length === 0) {
                listEl.innerHTML = '<div style="text-align:center;padding:3rem;color:var(--text-muted);">No security issues match your filter criteria.</div>';
                return;
            }

            filtered.forEach(f => {
                const card = document.createElement('div');
                card.className = 'finding-card';
                card.onclick = () => openDrawer(f);
                card.innerHTML = `
                    <div class="finding-header">
                        <span class="sev-badge ${f.severity}">${f.severity}</span>
                        <span class="finding-title">${f.vuln_type}</span>
                        <span class="finding-endpoint">${escapeHtml(f.endpoint)}</span>
                    </div>
                    <div class="finding-meta">
                        ${f.owasp_category} · ${f.file}${f.line > 0 ? ':' + f.line : ''} · Source: <strong>${f.source}</strong>
                    </div>
                    <div class="code-snippet">${escapeHtml(f.code_snippet || '(no direct snippet)')}</div>
                `;
                listEl.appendChild(card);
            });
        }

        /* ---------------- Slide-Over Drawer ---------------- */
        function openDrawer(f) {
            document.getElementById('drawerSevBadge').className = 'sev-badge ' + f.severity;
            document.getElementById('drawerSevBadge').textContent = f.severity;
            document.getElementById('drawerFindingType').textContent = f.vuln_type;
            document.getElementById('drawerEndpoint').textContent = f.endpoint;
            document.getElementById('drawerFile').textContent = f.file + (f.line > 0 ? ':' + f.line : '');
            document.getElementById('drawerOwasp').textContent = f.owasp_category + (f.cwe ? ' (CWE-' + f.cwe + ')' : '');
            document.getElementById('drawerSnippet').textContent = f.code_snippet || '(no code preview available)';
            document.getElementById('drawerWhy').textContent = f.explanation;
            document.getElementById('drawerFix').textContent = f.fix_recommendation;

            const diffEl = document.getElementById('drawerDiff');
            diffEl.innerHTML = '';
            if (f.fix_before && f.fix_after) {
                diffEl.innerHTML = `
                    <div class="diff-block before"><strong>- Vulnerable:</strong> ${escapeHtml(f.fix_before)}</div>
                    <div class="diff-block after"><strong>+ Remediated:</strong> ${escapeHtml(f.fix_after)}</div>
                `;
            }

            document.getElementById('findingDrawer').classList.add('open');
            document.getElementById('drawerBackdrop').classList.add('open');
        }

        function closeDrawer() {
            document.getElementById('findingDrawer').classList.remove('open');
            document.getElementById('drawerBackdrop').classList.remove('open');
        }

        /* ---------------- OWASP Breakdown ---------------- */
        function renderOwaspGrid(data) {
            const grid = document.getElementById('owaspGrid');
            grid.innerHTML = '';
            const categories = [
                { id: "A01", name: "Broken Access Control" },
                { id: "A02", name: "Cryptographic Failures" },
                { id: "A03", name: "Injection" },
                { id: "A05", name: "Security Misconfiguration" },
                { id: "A06", name: "Vulnerable Components" },
                { id: "A07", name: "Authentication Failures" },
                { id: "A08", name: "Software & Data Integrity" },
                { id: "A10", name: "SSRF" }
            ];

            categories.forEach(cat => {
                const count = data.findings.filter(f => f.owasp_category.includes(cat.id)).length;
                const card = document.createElement('div');
                card.className = 'owasp-card';
                card.innerHTML = `
                    <div class="owasp-card-header">
                        <span class="owasp-code">${cat.id}:2021</span>
                        <span class="sev-badge ${count > 0 ? 'HIGH' : 'LOW'}">${count} ${count === 1 ? 'Issue' : 'Issues'}</span>
                    </div>
                    <div class="owasp-name">${cat.name}</div>
                    <div class="owasp-bar-track">
                        <div class="owasp-bar-fill" style="width: ${Math.min(100, count * 25)}%; background: ${count > 0 ? 'var(--sev-high)' : 'var(--accent)'};"></div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        /* ---------------- Report Export ---------------- */
        function exportReport(format) {
            if (!currentScanResult) return;
            window.open(`/api/export/${format}?target=${encodeURIComponent(document.getElementById('targetInput').value)}`, '_blank');
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""
