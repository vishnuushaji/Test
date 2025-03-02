# src/models/models.py
from sqlalchemy import Column, String, DateTime, Enum, UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class ProcessingRequest(Base):
    __tablename__ = "processing_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='request_status'), 
                    default='PENDING')
    input_csv_path = Column(String, nullable=False)
    output_csv_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())