#audit business logic

from app.schemas.vulnerability import VulnerabilityOut
from fastapi import HTTPException, status
from typing import Dict, List, Any, Optional
import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.audit import Audit
from app.models.vulnerability import Vulnerability

logger = logging.getLogger(__name__)

DEFAULT_SEVERITY_LEVELS = ["critical", "high", "medium", "low", "info"]

def get_severity_counts():
    return {level: 0 for level in DEFAULT_SEVERITY_LEVELS}

def calculate_overall_severity(counts: Dict[str, int]) -> str:
    for level in ["critical", "high", "medium"]:
        if counts[level] > 0:
            return level
    return "low"

class AuditService:
    """Service for managing contract audits."""

    async def create_audit(
        self, 
        contract_id: int, 
        analyzers: List[str], 
        priority: str, 
        db: AsyncSession,
        parameters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Create a new audit record in the database."""
        audit = Audit(
            contract_id=contract_id,
            status="pending",
            parameters={"analyzers": analyzers, "priority": priority, **(parameters or {})},
            requested_at=datetime.datetime.now(),
            completed_at=None
        )
        db.add(audit)
        await db.commit()
        await db.refresh(audit)
        return audit.id

    async def get_audit(self, audit_id: int, db: AsyncSession) -> Audit:
        audit = await db.get(Audit, audit_id)
        if not audit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit ID '{audit_id}' not found")
        return audit

    async def update_audit_status(
        self, 
        audit_id: int, 
        status: str, 
        db: AsyncSession, 
        progress: Optional[int] = None
    ):
        audit = await self.get_audit(audit_id, db)
        audit.status = status
        if progress is not None:
            audit.progress = progress
        await db.commit()

    async def store_audit_results(
        self, 
        audit_id: int, 
        findings: List[Dict[str, Any]], 
        db: AsyncSession
    ):
        audit = await self.get_audit(audit_id, db)
        severity_counts = get_severity_counts()
        for finding in findings:
            severity = finding.get("severity", "info").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
            # Save finding to Vulnerability table
            vuln = Vulnerability(audit_id=audit_id, **finding)
            db.add(vuln)
        audit.completed_at = datetime.datetime.now()
        await db.commit()

    async def get_audit_results(self, audit_id: int, db: AsyncSession) -> Dict[str, Any]:
        audit = await self.get_audit(audit_id, db)
        result = await db.execute(select(Vulnerability).where(Vulnerability.audit_id == audit_id))
        findings = result.scalars().all()
        severity_counts = get_severity_counts()
        for finding in findings:
            severity = finding.severity.lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
        summary = {
            "total_findings": len(findings),
            "severity_counts": severity_counts,
            "overall_severity": calculate_overall_severity(severity_counts),
            "analyzers": audit.parameters.get("analyzers", []) if audit.parameters else []
        }
        return {
            "findings": [VulnerabilityOut.from_orm(f).dict() for f in findings],
            "findings_by_severity": severity_counts,
            "summary": summary
        }

    async def save_error(self, audit_id: int, error: str, db: AsyncSession):
        audit = await self.get_audit(audit_id, db)
        if not hasattr(audit, "errors") or audit.errors is None:
            audit.errors = []
        audit.errors.append({"timestamp": datetime.datetime.now().isoformat(), "error": error})
        await db.commit()

    async def add_tags(self, audit_id: int, tags: List[str], db: AsyncSession):
        audit = await self.get_audit(audit_id, db)
        if not hasattr(audit, "tags") or audit.tags is None:
            audit.tags = []
        audit.tags.extend(tags)
        await db.commit()

    async def update_progress(self, audit_id: int, progress: int, db: AsyncSession):
        audit = await self.get_audit(audit_id, db)
        audit.progress = progress
        await db.commit()