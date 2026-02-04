"""
Report Generator Module - Generate HTML and JSON reports.

This module handles:
- HTML dashboard generation
- JSON report output
- Console summary formatting
- Report history management
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate quality reports in multiple formats."""
    
    def __init__(self, config: Dict[str, Any], project_root: str):
        """
        Initialize the report generator.
        
        Args:
            config: Configuration dictionary for report generator
            project_root: Root directory of the project
        """
        self.config = config
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / config.get("output_dir", "quality_reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_reports(self, results: Dict[str, Any]):
        """
        Generate all configured reports.
        
        Args:
            results: Combined results from all modules
        """
        logger.info("Generating reports...")
        
        # Generate JSON report
        if self.config.get("generate_json", True):
            self._generate_json_report(results)
        
        # Generate HTML report
        if self.config.get("generate_html", True):
            self._generate_html_report(results)
        
        # Generate console summary
        if self.config.get("generate_console_summary", True):
            self._print_console_summary(results)
        
        # Save to history
        if self.config.get("save_history", True):
            self._save_to_history(results)
        
        logger.info(f"Reports generated in: {self.output_dir}")
    
    def _generate_json_report(self, results: Dict[str, Any]):
        """Generate JSON report."""
        logger.info("Generating JSON report...")
        
        report_file = self.output_dir / "latest_report.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "project_name": self.config.get("project_name", "Unknown"),
            "results": results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"JSON report saved to: {report_file}")
    
    def _generate_html_report(self, results: Dict[str, Any]):
        """Generate HTML dashboard report."""
        logger.info("Generating HTML report...")
        
        report_file = self.output_dir / "latest_report.html"
        
        # Extract results
        cleaner = results.get("code_cleaner", {})
        vuln = results.get("vulnerability_checker", {})
        conn = results.get("connection_tester", {})
        tester = results.get("code_tester", {})
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Quality Report - {self.config.get('project_name', 'Project')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            color: #666;
            font-size: 14px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .summary-card h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 14px;
        }}
        
        .metric-value {{
            font-weight: bold;
            font-size: 16px;
        }}
        
        .metric-value.success {{
            color: #10b981;
        }}
        
        .metric-value.warning {{
            color: #f59e0b;
        }}
        
        .metric-value.error {{
            color: #ef4444;
        }}
        
        .section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        
        .issue-list {{
            list-style: none;
        }}
        
        .issue-item {{
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #ddd;
            background: #f9fafb;
            border-radius: 4px;
        }}
        
        .issue-item.critical {{
            border-left-color: #dc2626;
            background: #fef2f2;
        }}
        
        .issue-item.high {{
            border-left-color: #f59e0b;
            background: #fffbeb;
        }}
        
        .issue-item.medium {{
            border-left-color: #3b82f6;
            background: #eff6ff;
        }}
        
        .issue-item.low {{
            border-left-color: #10b981;
            background: #f0fdf4;
        }}
        
        .issue-severity {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }}
        
        .severity-critical {{
            background: #dc2626;
            color: white;
        }}
        
        .severity-high {{
            background: #f59e0b;
            color: white;
        }}
        
        .severity-medium {{
            background: #3b82f6;
            color: white;
        }}
        
        .severity-low {{
            background: #10b981;
            color: white;
        }}
        
        .test-result {{
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .test-result.passed {{
            background: #f0fdf4;
            border-left: 4px solid #10b981;
        }}
        
        .test-result.failed {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
        }}
        
        .status-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .status-passed {{
            background: #10b981;
            color: white;
        }}
        
        .status-failed {{
            background: #ef4444;
            color: white;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Code Quality Report</h1>
            <p class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p class="timestamp">Project: {self.config.get('project_name', 'Unknown')}</p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>📝 Code Cleaning</h3>
                <div class="metric">
                    <span class="metric-label">Files Processed</span>
                    <span class="metric-value">{cleaner.get('total_files_processed', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Formatted</span>
                    <span class="metric-value success">{len(cleaner.get('formatted_files', []))}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Errors</span>
                    <span class="metric-value {'error' if cleaner.get('errors') else 'success'}">{len(cleaner.get('errors', []))}</span>
                </div>
            </div>
            
            <div class="summary-card">
                <h3>🔒 Security</h3>
                <div class="metric">
                    <span class="metric-label">Total Issues</span>
                    <span class="metric-value {'error' if vuln.get('total_issues', 0) > 0 else 'success'}">{vuln.get('total_issues', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Critical</span>
                    <span class="metric-value error">{vuln.get('severity_counts', {}).get('CRITICAL', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">High</span>
                    <span class="metric-value warning">{vuln.get('severity_counts', {}).get('HIGH', 0)}</span>
                </div>
            </div>
            
            <div class="summary-card">
                <h3>🔌 Connections</h3>
                <div class="metric">
                    <span class="metric-label">Total Tests</span>
                    <span class="metric-value">{conn.get('total_tests', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Passed</span>
                    <span class="metric-value success">{conn.get('passed_tests', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Failed</span>
                    <span class="metric-value {'error' if conn.get('failed_tests', 0) > 0 else 'success'}">{conn.get('failed_tests', 0)}</span>
                </div>
            </div>
            
            <div class="summary-card">
                <h3>✅ Tests</h3>
                <div class="metric">
                    <span class="metric-label">Total Tests</span>
                    <span class="metric-value">{tester.get('total_tests', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Coverage</span>
                    <span class="metric-value {'success' if tester.get('coverage_percentage', 0) >= 70 else 'warning'}">{tester.get('coverage_percentage', 0):.1f}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Pylint Score</span>
                    <span class="metric-value">{tester.get('pylint_results', {}).get('score', 'N/A')}/10</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔒 Security Vulnerabilities</h2>
            {self._generate_vulnerability_html(vuln)}
        </div>
        
        <div class="section">
            <h2>🔌 Connection Tests</h2>
            {self._generate_connection_html(conn)}
        </div>
        
        <div class="footer">
            <p>Generated by Code Quality Agent</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"HTML report saved to: {report_file}")
    
    def _generate_vulnerability_html(self, vuln: Dict[str, Any]) -> str:
        """Generate HTML for vulnerability section."""
        if vuln.get('total_issues', 0) == 0:
            return '<p style="color: #10b981; font-weight: bold;">✓ No security issues found!</p>'
        
        html = '<ul class="issue-list">'
        
        # Bandit issues
        for issue in vuln.get('bandit_issues', [])[:10]:  # Limit to 10
            severity = issue.get('severity', 'LOW').lower()
            html += f'''
            <li class="issue-item {severity}">
                <span class="issue-severity severity-{severity}">{issue.get('severity', 'LOW')}</span>
                <strong>{issue.get('issue', 'Unknown issue')}</strong>
                <br><small>{issue.get('file', '')}:{issue.get('line', '')}</small>
            </li>
            '''
        
        # Custom checks
        for issue in vuln.get('custom_checks', []):
            severity = issue.get('severity', 'LOW').lower()
            html += f'''
            <li class="issue-item {severity}">
                <span class="issue-severity severity-{severity}">{issue.get('severity', 'LOW')}</span>
                <strong>{issue.get('issue', 'Unknown issue')}</strong>
                <br><small>{issue.get('file', '')}</small>
                <br><small style="color: #666;">{issue.get('recommendation', '')}</small>
            </li>
            '''
        
        html += '</ul>'
        return html
    
    def _generate_connection_html(self, conn: Dict[str, Any]) -> str:
        """Generate HTML for connection tests section."""
        if conn.get('total_tests', 0) == 0:
            return '<p style="color: #666;">No connection tests were run.</p>'
        
        html = ''
        
        # Database tests
        for test in conn.get('database_tests', []):
            status = test.get('status', 'FAILED').lower()
            html += f'''
            <div class="test-result {status}">
                <span>{test.get('test', 'Database Test')}</span>
                <span class="status-badge status-{status}">{test.get('status', 'UNKNOWN')}</span>
            </div>
            '''
        
        # API tests
        for test in conn.get('api_tests', [])[:5]:  # Limit to 5
            status = test.get('status', 'FAILED').lower()
            html += f'''
            <div class="test-result {status}">
                <span>{test.get('test', 'API Test')}</span>
                <span class="status-badge status-{status}">{test.get('status', 'UNKNOWN')}</span>
            </div>
            '''
        
        return html
    
    def _print_console_summary(self, results: Dict[str, Any]):
        """Print a summary to console."""
        print("\n" + "="*70)
        print("CODE QUALITY REPORT SUMMARY")
        print("="*70)
        
        # Code Cleaner
        cleaner = results.get("code_cleaner", {})
        print(f"\n📝 CODE CLEANING:")
        print(f"   Files processed: {cleaner.get('total_files_processed', 0)}")
        print(f"   Formatted: {len(cleaner.get('formatted_files', []))}")
        
        # Vulnerabilities
        vuln = results.get("vulnerability_checker", {})
        print(f"\n🔒 SECURITY:")
        print(f"   Total issues: {vuln.get('total_issues', 0)}")
        print(f"   Critical: {vuln.get('severity_counts', {}).get('CRITICAL', 0)}")
        print(f"   High: {vuln.get('severity_counts', {}).get('HIGH', 0)}")
        
        # Connections
        conn = results.get("connection_tester", {})
        print(f"\n🔌 CONNECTIONS:")
        print(f"   Tests run: {conn.get('total_tests', 0)}")
        print(f"   Passed: {conn.get('passed_tests', 0)}")
        print(f"   Failed: {conn.get('failed_tests', 0)}")
        
        # Tests
        tester = results.get("code_tester", {})
        print(f"\n✅ CODE TESTS:")
        print(f"   Total tests: {tester.get('total_tests', 0)}")
        print(f"   Coverage: {tester.get('coverage_percentage', 0):.1f}%")
        print(f"   Pylint score: {tester.get('pylint_results', {}).get('score', 'N/A')}/10")
        
        print("\n" + "="*70)
        print(f"Full reports available in: {self.output_dir}")
        print("="*70 + "\n")
    
    def _save_to_history(self, results: Dict[str, Any]):
        """Save report to history."""
        history_dir = self.output_dir / "history"
        history_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = history_dir / f"report_{timestamp}.json"
        
        with open(history_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Clean old history files
        max_history = self.config.get("max_history_reports", 10)
        history_files = sorted(history_dir.glob("report_*.json"))
        
        if len(history_files) > max_history:
            for old_file in history_files[:-max_history]:
                old_file.unlink()
