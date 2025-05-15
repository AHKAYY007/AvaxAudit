from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class AuditBase(BaseModel):
    contract_id: int
    status: Optional[str] = "pending"
    parameters: Optional[Any] = None

class AuditCreate(AuditBase):
    pass

class AuditUpdate(BaseModel):
    status: Optional[str]
    completed_at: Optional[datetime]
    parameters: Optional[Any]

class Audit(AuditBase):
    id: int
    requested_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True