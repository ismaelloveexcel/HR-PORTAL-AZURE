"""Census Verification Token model for employee self-service verification."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.renewal import Base


class CensusVerificationToken(Base):
    """Token for employees to verify their insurance census data without login."""
    
    __tablename__ = "census_verification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    
    # Unique token for URL access
    token = Column(String(100), unique=True, index=True, nullable=False)
    
    # Link to census record
    census_record_id = Column(Integer, ForeignKey("insurance_census_records.id", ondelete="CASCADE"), nullable=False)
    
    # Link to employee (for email)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    # Token status
    is_used = Column(Boolean, default=False, nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False)
    
    # Verification tracking
    email_sent = Column(Boolean, default=False, nullable=False)
    email_sent_at = Column(DateTime, nullable=True)
    email_address = Column(String(255), nullable=True)
    
    # Employee response
    verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    updates_submitted = Column(Boolean, default=False, nullable=False)
    
    # Reminder tracking
    reminder_count = Column(Integer, default=0, nullable=False)
    last_reminder_at = Column(DateTime, nullable=True)
    
    # Expiry
    expires_at = Column(DateTime, nullable=False)
    
    # Audit
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String(50), nullable=True)
    
    # Relationships
    census_record = relationship("InsuranceCensusRecord", foreign_keys=[census_record_id])
    employee = relationship("Employee", foreign_keys=[employee_id])

    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'census_record_id': self.census_record_id,
            'employee_id': self.employee_id,
            'is_used': self.is_used,
            'is_expired': self.is_expired,
            'email_sent': self.email_sent,
            'email_sent_at': self.email_sent_at.isoformat() if self.email_sent_at else None,
            'email_address': self.email_address,
            'verified': self.verified,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'updates_submitted': self.updates_submitted,
            'reminder_count': self.reminder_count,
            'last_reminder_at': self.last_reminder_at.isoformat() if self.last_reminder_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
        }
