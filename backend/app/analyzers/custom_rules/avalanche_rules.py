from typing import Dict, List, Any
import re

class AvaxRuleEngine:
    """Rules specific to Avalanche network."""
    
    def __init__(self, rules=None):
        self.rules = rules or [
            self.check_gas_price_usage,
            self.check_time_assumptions,
            self.check_bridge_security,
            self.check_subnet_compatibility,
        ]
    
    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        """Run all Avalanche-specific rules on source code."""
        if not source_code:
            return []
            
        findings = []
        for rule in self.rules:
            result = rule(source_code)
            if result:
                findings.extend(result)
                
        return findings
    
    def check_gas_price_usage(self, source_code: str) -> List[Dict[str, Any]]:
        """Check for hardcoded gas prices not suitable for Avalanche."""
        findings = []
        
        # Look for hardcoded gas prices
        hardcoded_gas = re.search(r'gasPrice\s*:\s*(\d+)', source_code)
        if hardcoded_gas:
            findings.append({
                "title": "Hardcoded Gas Price",
                "description": "Contract uses hardcoded gas prices which may not be optimal for Avalanche's fee structure.",
                "severity": "medium",
                "line": None,  # Would need more sophisticated parsing to get line number
                "rule_id": "AVAX-GAS-001",
            })
            
        return findings
    
    def check_time_assumptions(self, source_code: str) -> List[Dict[str, Any]]:
        """Check for time assumptions that may not hold on Avalanche."""
        findings = []
        
        # Look for block.timestamp used with large time windows
        if re.search(r'block\.timestamp.+\+\s*(\d+)', source_code):
            time_values = re.findall(r'block\.timestamp.+\+\s*(\d+)', source_code)
            for value in time_values:
                if int(value) > 86400:  # More than a day
                    findings.append({
                        "title": "Long Time Window Assumption",
                        "description": "Contract uses long time windows with block.timestamp. Avalanche has faster block times than Ethereum, consider adjusting time assumptions.",
                        "severity": "info",
                        "rule_id": "AVAX-TIME-001",
                    })
                    break
                    
        return findings
    
    def check_bridge_security(self, source_code: str) -> List[Dict[str, Any]]:
        """Check for secure bridge interactions."""
        findings = []
        
        # Check for bridge contracts usage
        bridge_patterns = [
            r'bridge\.avax',
            r'AvaxBridge',
            r'0x8eb8.+', # Example bridge contract address pattern
        ]
        
        for pattern in bridge_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                findings.append({
                    "title": "Bridge Interaction Detected",
                    "description": "Contract interacts with cross-chain bridges. Ensure proper validation of bridge messages and handle bridge downtime gracefully.",
                    "severity": "high",
                    "rule_id": "AVAX-BRIDGE-001",
                })
                break
                
        return findings
    
    def check_subnet_compatibility(self, source_code: str) -> List[Dict[str, Any]]:
        """Check for subnet compatibility issues."""
        findings = []
        
        # Check for precompiled contract usage that may not exist on subnets
        if re.search(r'0x0000000000000000000000000000000000000[1-9]', source_code):
            findings.append({
                "title": "Precompiled Contract Usage",
                "description": "Contract uses Ethereum precompiled contracts that may not be available on all Avalanche subnets.",
                "severity": "medium",
                "rule_id": "AVAX-SUBNET-001",
            })
            
        return findings