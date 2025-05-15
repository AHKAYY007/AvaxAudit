from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportBase(BaseModel):
    audit_id: int
    format: str
    content: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    generated_at: datetime

    class Config:
        orm_mode = True