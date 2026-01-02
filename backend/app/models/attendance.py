from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.renewal import Base


class AttendanceRecord(Base):
    """Attendance record for tracking employee clock in/out, GPS, overtime, and WFH."""

    __tablename__ = "attendance_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    
    # Date of attendance
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    # Clock in/out times
    clock_in: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    clock_out: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # GPS coordinates for clock in
    clock_in_latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8), nullable=True)
    clock_in_longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(11, 8), nullable=True)
    clock_in_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # GPS coordinates for clock out
    clock_out_latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8), nullable=True)
    clock_out_longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(11, 8), nullable=True)
    clock_out_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Work type: office, wfh (work from home), field, leave
    work_type: Mapped[str] = mapped_column(String(20), default="office", nullable=False)
    
    # WFH specific fields
    wfh_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wfh_approved: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    wfh_approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    wfh_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Calculated hours
    total_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)
    regular_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)
    overtime_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)
    
    # Overtime type: none, pre-approved, auto-calculated
    overtime_type: Mapped[str] = mapped_column(String(20), default="none", nullable=False)
    overtime_approved: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    overtime_approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    overtime_approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Break time tracking
    break_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    break_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    break_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Status: pending, present, absent, late, half-day, on-leave
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    
    # Late arrival tracking
    is_late: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    late_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    late_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Early departure tracking
    is_early_departure: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    early_departure_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    early_departure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Notes and remarks
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], backref="attendance_records")
    wfh_approver = relationship("Employee", foreign_keys=[wfh_approved_by])
    overtime_approver = relationship("Employee", foreign_keys=[overtime_approved_by])


# Work type constants
WORK_TYPES = ["office", "wfh", "field", "leave", "holiday"]

# Attendance status constants
ATTENDANCE_STATUSES = ["pending", "present", "absent", "late", "half-day", "on-leave", "holiday"]

# Overtime types
OVERTIME_TYPES = ["none", "pre-approved", "auto-calculated", "requested"]

# Standard work hours (UAE)
STANDARD_WORK_HOURS = 8
STANDARD_CLOCK_IN = time(8, 0)  # 8:00 AM
STANDARD_CLOCK_OUT = time(17, 0)  # 5:00 PM
GRACE_PERIOD_MINUTES = 15  # 15 minutes grace period for late arrivals
