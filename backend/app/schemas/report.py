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
        from_attributes = True  # Use this for Pydantic v2+

class ReportOut(BaseModel):
    id: int
    audit_id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Use this for Pydantic v2+