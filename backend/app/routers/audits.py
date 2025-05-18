#audit initiation and results

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.audit_service import AuditService
from app.tasks.audit_tasks import run_audit_task
from app.db.database import get_async_session
import uuid

router = APIRouter(
    prefix="/audits",
    tags=["audits"],
)

audit_service = AuditService()

class AuditRequest(BaseModel):
    contract_id: int
    analyzers: List[str] = Field(default_factory=lambda: ["slither", "custom"])  # Default analyzers
    priority: str = "normal"

@router.post("/start")
async def start_audit(
    audit_request: AuditRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session)
):
    """Start audit process for a contract."""
    try:
        # Create audit record in DB
        audit_id = await audit_service.create_audit(
            contract_id=audit_request.contract_id,
            analyzers=audit_request.analyzers,
            priority=audit_request.priority,
            db=db
        )

        # Start audit in background
        background_tasks.add_task(
            run_audit_task,
            audit_id=audit_id,
            contract_id=audit_request.contract_id,
            analyzers=audit_request.analyzers
        )

        return {
            "audit_id": audit_id,
            "status": "started",
            "message": "Audit has been started. Check results with the audit_id."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{audit_id}")
async def get_audit_status(
    audit_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get status of an audit."""
    try:
        audit = await audit_service.get_audit(audit_id, db)
        if not audit:
            raise HTTPException(status_code=404, detail="Audit not found")

        return {
            "audit_id": audit.id,
            "status": audit.status,
            "progress": audit.progress,
            "started_at": audit.requested_at,
            "completed_at": audit.completed_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{audit_id}/results")
async def get_audit_results(
    audit_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Get detailed results of an audit."""
    try:
        audit = await audit_service.get_audit(audit_id, db)
        if not audit:
            raise HTTPException(status_code=404, detail="Audit not found")

        if audit.status != "completed":
            return {
                "audit_id": audit.id,
                "status": audit.status,
                "progress": audit.progress,
                "message": "Audit is still in progress or failed."
            }

        # Get detailed results
        results = await audit_service.get_audit_results(audit_id, db)

        return {
            "audit_id": audit.id,
            "status": "completed",
            "contract_id": audit.contract_id,
            "findings_count": len(results["findings"]),
            "findings_by_severity": results["findings_by_severity"],
            "findings": results["findings"],
            "summary": results["summary"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))