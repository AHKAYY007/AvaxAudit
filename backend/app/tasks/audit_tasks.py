import asyncio
import logging
import time
from typing import List, Dict, Any

from app.services.audit_service import AuditService
from app.services.contract_service import ContractService
from app.analyzers.slither_analyzer import SlitherAnalyzer
from app.analyzers.custom_rules.avalanche_rules import AvaxRuleEngine

logger = logging.getLogger(__name__)

# Services
audit_service = AuditService()
contract_service = ContractService()

# Analyzers
slither_analyzer = SlitherAnalyzer()
avax_rules = AvaxRuleEngine()

ANALYZER_MAP = {
    "slither": slither_analyzer,
    "avax_rules": avax_rules,
}

async def run_audit_task(audit_id: int, contract_id: int, analyzers: List[str]) -> None:
    """Run audit task in background."""
    start_time = time.time()
    try:
        # Input validation
        if not analyzers:
            logger.warning(f"No analyzers selected for audit {audit_id}")
            await audit_service.update_audit_status(audit_id, "skipped")
            return

        await audit_service.update_audit_status(audit_id, "running")

        # Fetch contract details
        contract = await contract_service.get_contract_by_id(contract_id)
        if not contract:
            await audit_service.update_audit_status(audit_id, "failed")
            logger.error(f"Contract {contract_id} not found.")
            return

        findings = []

        # Run selected analyzers using the map
        for analyzer_key in analyzers:
            analyzer = ANALYZER_MAP.get(analyzer_key)
            if not analyzer:
                logger.warning(f"Unknown analyzer '{analyzer_key}' for audit {audit_id}")
                continue
            try:
                result = await analyzer.analyze(contract.source_code)
                findings.extend(result)
            except Exception as analyzer_exc:
                logger.exception(f"Analyzer '{analyzer_key}' failed for audit {audit_id}: {analyzer_exc}")

        # Save findings to audit
        await audit_service.save_findings(audit_id, findings)

        # Optionally generate a report
        await audit_service.generate_report(audit_id, findings)

        # Update status to completed
        await audit_service.update_audit_status(audit_id, "completed")
        duration = time.time() - start_time
        logger.info(f"Audit {audit_id} completed successfully in {duration:.2f}s.")

    except Exception as e:
        logger.exception(f"Error running audit task for audit_id={audit_id}: {e}")
        await audit_service.update_audit_status(audit_id, "failed")
        await audit_service.save_error(audit_id, str(e))
        logger.error(f"Audit {audit_id} failed with error: {e}")