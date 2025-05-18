from sqlalchemy.sql.sqltypes import String, DateTime, Text
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy import func


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(42), unique=True, nullable=False, index=True)
    chain = Column(String(50), nullable=False)
    source_code = Column(Text, nullable=True)
    bytecode = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    audits = relationship("Audit", back_populates="contract")
