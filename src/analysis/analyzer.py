"""Security analysis and reporting"""

from typing import Dict, List
import json
from datetime import datetime

class SecurityAnalyzer:
    """Analyze security findings and generate reports"""
    
    def __init__(self):
        self.findings = []
    
    def add_finding(self, severity: str, title: str, description: str):
        """Add a security finding"""
        finding = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "title": title,
            "description": description,
        }
        self.findings.append(finding)
    
    def generate_report(self) -> Dict:
        """Generate security report"""
        critical = len([f for f in self.findings if f["severity"] == "CRITICAL"])
        high = len([f for f in self.findings if f["severity"] == "HIGH"])
        medium = len([f for f in self.findings if f["severity"] == "MEDIUM"])
        low = len([f for f in self.findings if f["severity"] == "LOW"])
        
        return {
            "report_date": datetime.now().isoformat(),
            "summary": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
                "total": len(self.findings),
            },
            "findings": self.findings,
        }
    
    def export_json(self, filepath: str):
        """Export report as JSON"""
        report = self.generate_report()
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
