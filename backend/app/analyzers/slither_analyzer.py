import json
import tempfile
import os
import subprocess
from typing import Dict, List, Any

from app.analyzers.base import BaseAnalyzer

class SlitherAnalyzer(BaseAnalyzer):
    """Integration with Slither static analyzer."""
    
    def __init__(self):
        super().__init__("slither")
        
    async def analyze(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run Slither analysis on contract."""
        if not contract_data.get("source") or not contract_data["source"].get("source_code"):
            return [{
                "title": "Source Not Available",
                "description": "Contract source code is not verified. Cannot perform Slither analysis.",
                "severity": "info",
                "rule_id": "SLITHER-000",
            }]
            
        # Create temporary file with contract source
        with tempfile.NamedTemporaryFile(suffix='.sol', delete=False) as temp:
            temp.write(contract_data["source"]["source_code"].encode('utf-8'))
            temp_path = temp.name
            
        try:
            # Run slither analysis
            cmd = f"slither {temp_path} --json -"
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                return [{
                    "title": "Slither Analysis Failed",
                    "description": f"Error running Slither: {stderr}",
                    "severity": "error",
                    "rule_id": "SLITHER-ERR",
                }]
                
            # Parse results
            try:
                results = json.loads(stdout)
                findings = []
                
                for detector in results.get("detectors", []):
                    findings.append({
                        "title": detector.get("check", "Unknown Issue"),
                        "description": detector.get("description", "No description available"),
                        "severity": detector.get("impact", "medium").lower(),
                        "line": detector.get("first_line_number"),
                        "rule_id": f"SLITHER-{detector.get('check', 'UNK')}",
                    })
                    
                return findings
            except json.JSONDecodeError:
                return [{
                    "title": "Slither Output Parsing Failed",
                    "description": "Could not parse Slither output.",
                    "severity": "error",
                    "rule_id": "SLITHER-PARSE-ERR",
                }]
                
        finally:
            # Clean up temp file
            os.unlink(temp_path)
            
    def get_analyzer_info(self) -> Dict[str, Any]:
        """Return information about this analyzer."""
        return {
            "name": self.name,
            "description": "Slither is a Solidity static analysis framework",
            "capabilities": [
                "Detect vulnerabilities",
                "Enhance code quality",
                "Security best practices"
            ],
            "version": "0.8.10"  # Replace with actual version
        }