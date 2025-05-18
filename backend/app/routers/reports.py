# report generation and export

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.services.report_service import ReportService
from typing import List
from app.schemas.report import ReportOut  # Make sure this exists
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

report_service = ReportService()

@router.get('/', response_model=List[ReportOut])
async def list_reports(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):
    """List all reports with pagination."""
    try:
        reports = await report_service.list_reports(db, skip=skip, limit=limit)
        return reports
    except Exception as e:
        logger.exception("Failed to list reports")
        raise HTTPException(status_code=500, detail="Failed to retrieve reports.")
    

@router.get("/export/csv")
async def export_csv(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await report_service.export_reports_csv(db, skip, limit)
    except Exception as e:
        logger.exception("Failed to export reports as CSV")
        raise HTTPException(status_code=500, detail="CSV export failed.")

@router.get("/export/pdf")
async def export_pdf(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        return await report_service.export_reports_pdf(db, skip, limit)
    except Exception as e:
        logger.exception("Failed to export reports as PDF")
        raise HTTPException(status_code=500, detail="PDF export failed.")
