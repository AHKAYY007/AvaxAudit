from sqlalchemy.sql.sqltypes import String, DateTime, JSON
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import func

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    requested_at = Column(DateTime, default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    parameters = Column(JSON, nullable=True)
    progress = Column(Float, nullable=True)
    errors = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)

    contract = relationship("Contract", back_populates="audits")
    vulnerabilities = relationship("Vulnerability", back_populates="audit")
    reports = relationship("Report", back_populates="audit")