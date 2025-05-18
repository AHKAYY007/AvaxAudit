from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.db.database import get_async_session
from app.models.vulnerability import Vulnerability
from app.schemas.vulnerability import VulnerabilityOut, VulnerabilityUpdate
from typing import List, Optional

router = APIRouter(
    prefix="/vulnerabilities",
    tags=["vulnerabilities"]
)

@router.get("/", response_model=List[VulnerabilityOut])
async def get_vulnerabilities(
    audit_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_session)
):
    """Get vulnerabilities for a given audit ID or filter by severity."""
    query = select(Vulnerability)
    if audit_id:
        query = query.where(Vulnerability.audit_id == audit_id)
    if severity:
        query = query.where(Vulnerability.severity == severity)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{finding_id}", response_model=VulnerabilityOut)
async def get_finding(finding_id: int, db: AsyncSession = Depends(get_async_session)):
    """Get a specific vulnerability by ID."""
    result = await db.get(Vulnerability, finding_id)
    if not result:
        raise HTTPException(status_code=404, detail="Finding not found")
    return result

@router.patch("/{finding_id}", response_model=VulnerabilityOut)
async def update_finding(
    finding_id: int,
    update: VulnerabilityUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update a vulnerability (e.g., mark as acknowledged or add a note)."""
    vuln = await db.get(Vulnerability, finding_id)
    if not vuln:
        raise HTTPException(status_code=404, detail="Finding not found")
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vuln, key, value)
    await db.commit()
    await db.refresh(vuln)
    return vuln