from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContractBase(BaseModel):
    address: str
    chain: str
    source_code: Optional[str] = None
    bytecode: Optional[str] = None

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContractOut(BaseModel):
    id: int
    address: Optional[str]
    chain: str
    source_code: Optional[str]
    bytecode: Optional[str]
    created_at: datetime

    class Config:
         from_attributes = True