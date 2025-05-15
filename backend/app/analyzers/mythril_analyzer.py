import json
import tempfile
import os
import subprocess
from typing import Dict, List, Any

from app.analyzers.base import BaseAnalyzer

class MythrilAnalyzer(BaseAnalyzer):
    """Integration with Mythril symbolic analysis tool."""

    def __init__(self):
        super().__init__("mythril")

    async def analyze(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # 1. Verify we have source
        source = contract_data.get("source", {}).get("source_code")
        if not source:
            return [{
                "title": "Source Not Available",
                "description": "Contract source code is not verified. Cannot perform Mythril analysis.",
                "severity": "info",
                "rule_id": "MYTH-000",
            }]

        # 2. Write to a temp file
        with tempfile.NamedTemporaryFile(suffix=".sol", delete=False) as tf:
            tf.write(source.encode("utf-8"))
            tf.flush()
            temp_path = tf.name

        try:
            # 3. Invoke Mythril CLI to produce JSON
            cmd = [
                "myth", "analyze", temp_path,
                "--execution-timeout", "60",
                "--solver-timeout", "60",
                "--max-depth", "50",
                "--output", "json"
            ]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = proc.communicate()

            # 4. Error handling
            if proc.returncode != 0:
                return [{
                    "title": "Mythril Analysis Failed",
                    "description": f"Error running Mythril: {stderr.strip()}",
                    "severity": "error",
                    "rule_id": "MYTH-ERR",
                }]

            # 5. Parse JSON results
            try:
                data = json.loads(stdout)
            except json.JSONDecodeError:
                return [{
                    "title": "Mythril Output Parsing Failed",
                    "description": "Could not decode Mythril JSON output.",
                    "severity": "error",
                    "rule_id": "MYTH-PARSE-ERR",
                }]

            findings: List[Dict[str, Any]] = []
            for issue in data.get("issues", []):
                findings.append({
                    "title": issue.get("title", "Unknown Issue"),
                    "description": issue.get("description", "No description provided."),
                    "severity": issue.get("severity", "Medium").lower(),
                    "line": issue.get("location", {}).get("source_line"),
                    "rule_id": f"MYTH-{issue.get('swc_id', issue.get('check_id', 'UNK'))}",
                })

            return findings

        finally:
            # 6. Clean up
            os.unlink(temp_path)

    def get_analyzer_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "Mythril is a security analysis tool for EVM bytecode",
            "capabilities": [
                "Symbolic execution",
                "Path explosion detection",
                "SWC vulnerability classification"
            ],
            "version": "1.11.8"  # sync with your installed version
        }
