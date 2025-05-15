# analyzers/custom_rules/gas_rules.py

import re
from typing import List, Dict, Any

def check_hardcoded_gas_price(source_code: str) -> List[Dict[str, Any]]:
    """Detect `gasPrice: <number>` literals."""
    findings = []
    for m in re.finditer(r'gasPrice\s*:\s*(\d+)', source_code):
        findings.append({
            "rule_id": "GAS-AVAX-001",
            "title": "Hardcoded Gas Price",
            "description": (
                "Found literal gasPrice; "
                "Avalanche’s dynamic fee markets mean you should use `tx.gasPrice = provider.getGasPrice()`."
            ),
            "severity": "medium",
            "line": source_code[:m.start()].count("\n") + 1
        })
    return findings

def check_unbounded_gas_limit(source_code: str) -> List[Dict[str, Any]]:
    """Detect excessively high or missing gasLimit specifications."""
    findings = []
    # simplistic example
    if re.search(r'gasLimit\s*:\s*0x[0-9a-fA-F]{6,}', source_code):
        findings.append({
            "rule_id": "GAS-AVAX-002",
            "title": "Excessive Gas Limit",
            "description": (
                "Gas limit looks hard-coded or excessively large; "
                "consider estimating with `provider.estimateGas(tx)`."
            ),
            "severity": "low",
        })
    return findings

# Export a list of all gas rules to make loading easy
ALL_GAS_RULES = [
    check_hardcoded_gas_price,
    check_unbounded_gas_limit,
    # add more as needed
]
