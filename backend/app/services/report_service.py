#report generation

from fastapi.responses import StreamingResponse
import csv
import io
from fpdf import FPDF
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import Report

def report_to_dict(report):
    return {
        key: value
        for key, value in vars(report).items()
        if not key.startswith("_")
    }

class ReportService:

    async def list_reports(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Report).offset(skip).limit(limit))
        return result.scalars().all()

    async def export_reports_csv(self, db: AsyncSession, skip=0, limit=100):
        reports = await self.list_reports(db, skip, limit)
        output = io.StringIO()
        writer = csv.writer(output)

        if not reports:
            writer.writerow(["No reports found"])
        else:
            report_dicts = [report_to_dict(r) for r in reports]
            writer = csv.DictWriter(output, fieldnames=report_dicts[0].keys())
            writer.writeheader()
            for row in report_dicts:
                writer.writerow(row)

        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=reports.csv"
        })

    async def export_reports_pdf(self, db: AsyncSession, skip=0, limit=100):
        reports = await self.list_reports(db, skip, limit)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        for report in reports:
            report_data = report_to_dict(report)
            for key, value in report_data.items():
                pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)
            pdf.ln(5)

        output = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        output.write(pdf_bytes)
        output.seek(0)

        return StreamingResponse(output, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=reports.pdf"
        })
