# analyzers/rule_engine.py

import importlib
import pkgutil
import inspect
from typing import List, Dict, Any

# You could also hard-code imports if you prefer explicitness
from custom_rules.avalanche_rules import AvaxRuleEngine
from custom_rules.gas_rules import ALL_GAS_RULES
from custom_rules.security_rules import ALL_SECURITY_RULES

class RuleEngine:
    def __init__(self):
        # flatten into one list of callables
        self.rule_functions = []
        
        # Avalanche-specialized engine (if you want to keep that class)
        self.avax_engine = AvaxRuleEngine()
        self.rule_functions.extend(self.avax_engine.rules)
        
        # your new modules
        self.rule_functions.extend(ALL_GAS_RULES)
        self.rule_functions.extend(ALL_SECURITY_RULES)
        
        # (Optionally) auto-discover any other modules in custom_rules
        # for finder in pkgutil.iter_modules([path_to_custom_rules]):
        #     module = importlib.import_module(f"custom_rules.{finder.name}")
        #     for _, fn in inspect.getmembers(module, inspect.isfunction):
        #         if fn.__module__ == module.__name__:
        #             self.rule_functions.append(fn)

    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        for fn in self.rule_functions:
            try:
                result = fn(source_code)
                if result:
                    findings.extend(result)
            except Exception as e:
                findings.append({
                    "rule_id": "ENGINE-ERROR",
                    "title": f"Error running {fn.__name__}",
                    "description": str(e),
                    "severity": "error",
                })
        # optional: sort by severity or rule_id, add timestamps, etc.
        return findings

# usage
# engine = RuleEngine()
# findings = engine.analyze(solidity_source_code)
