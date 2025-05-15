# analyzers/custom_rules/security_rules.py

import re
from typing import Dict, List, Any

def check_reentrancy(source_code: str) -> List[Dict[str, Any]]:
    """Detect patterns prone to reentrancy (e.g. external call before state update)."""
    findings = []
    # VERY simplified example; for real use AST
    pattern = re.compile(r'(call|transfer)\(.*\)\s*;\s*.*_\.balance')
    if pattern.search(source_code):
        findings.append({
            "rule_id": "SEC-001",
            "title": "Potential Reentrancy",
            "description": (
                "Looks like an external call occurs before state updates. "
                "Use checks-effects-interactions or a reentrancy guard."
            ),
            "severity": "high",
        })
    return findings

def check_integer_overflow(source_code: str) -> List[Dict[str, Any]]:
    """Warn when arithmetic is done without SafeMath (on older Solidity)."""
    findings = []
    if re.search(r'\+\+|\-\-', source_code) and "SafeMath" not in source_code:
        findings.append({
            "rule_id": "SEC-002",
            "title": "Unchecked Arithmetic",
            "description": "Arithmetic operations aren’t protected by overflow checks; use SafeMath or Solidity ^0.8.0+.",
            "severity": "medium",
        })
    return findings

def check_bridge_message_validation(source_code: str) -> List[Dict[str, Any]]:
    """Avalanche-specific: ensure inbound bridge messages are properly authenticated."""
    findings = []
    if "validateBridgeMessage" not in source_code and "bridge" in source_code.lower():
        findings.append({
            "rule_id": "SEC-AVAX-001",
            "title": "Missing Bridge Message Validation",
            "description": (
                "Contract interacts with a bridge but doesn’t call `validateBridgeMessage(...)`. "
                "This can allow forged cross-chain messages."
            ),
            "severity": "high",
        })
    return findings

ALL_SECURITY_RULES = [
    check_reentrancy,
    check_integer_overflow,
    check_bridge_message_validation,
]
