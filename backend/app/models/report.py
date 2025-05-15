from sqlalchemy.sql.sqltypes import String, DateTime, Text
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import func

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False)
    generated_at = Column(DateTime, default=func.now(), nullable=False)
    format = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)

    audit = relationship("Audit", back_populates="reports")