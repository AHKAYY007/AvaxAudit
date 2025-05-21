import asyncio
import logging
import time
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.audit_service import AuditService
from app.services.contract_service import ContractService
from app.analyzers.slither_analyzer import SlitherAnalyzer
from app.analyzers.mythril_analyzer import MythrilAnalyzer
from app.analyzers.custom_rules.gas_rules import ALL_GAS_RULES
from app.analyzers.custom_rules.security_rules import ALL_SECURITY_RULES
from app.analyzers.custom_rules.avalanche_rules import AvaxRuleEngine
from app.db.database import get_async_session

logger = logging.getLogger(__name__)

# Services
audit_service = AuditService()
contract_service = ContractService()

# Analyzers
slither_analyzer = SlitherAnalyzer()
avax_rules = AvaxRuleEngine()
mythril_analyzer = MythrilAnalyzer()
gas_rule_engine = AvaxRuleEngine(ALL_GAS_RULES)
security_rule_engine = AvaxRuleEngine(ALL_SECURITY_RULES)

ANALYZER_MAP = {
    "slither": slither_analyzer,
    "custom": avax_rules,
    "mythril": mythril_analyzer,
    "gas_rules": gas_rule_engine,
    "security_rules": security_rule_engine,
}

async def run_audit_task(audit_id: int, contract_id: int, analyzers: List[str]) -> None:
    """Run audit task in background."""

    start_time = time.time()
    db_gen = get_async_session()
    db = await anext(db_gen)
    try:
        # Input validation
        if not analyzers:
            logger.warning(f"No analyzers selected for audit {audit_id}")
            await audit_service.update_audit_status(audit_id, "skipped", db)
            return

        await audit_service.update_audit_status(audit_id, "running", db)

        # Fetch contract details
        contract = await contract_service.get_contract_by_id(contract_id, db)
        if not contract:
            await audit_service.update_audit_status(audit_id, "failed", db)
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
                result = await analyzer.analyze({
                    "source": {"source_code": contract.source_code},
                })
                findings.extend(result)
            except Exception as analyzer_exc:
                logger.exception(f"Analyzer '{analyzer_key}' failed for audit {audit_id}: {analyzer_exc}")

        # Save findings to audit
        await audit_service.store_audit_results(audit_id, findings, db)

        # Optionally generate a report
        # await audit_service.generate_report(audit_id, findings, db)

        # Update status to completed
        await audit_service.update_audit_status(audit_id, "completed", db)
        duration = time.time() - start_time
        logger.info(f"Audit {audit_id} completed successfully in {duration:.2f}s.")

    except Exception as e:
        logger.exception(f"Error running audit task for audit_id={audit_id}: {e}")
        await audit_service.update_audit_status(audit_id, "failed", db)
        await audit_service.save_error(audit_id, str(e), db)
        logger.error(f"Audit {audit_id} failed with error: {e}")
    finally:
        await db_gen.aclose()