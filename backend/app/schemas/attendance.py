from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class ClockInRequest(BaseModel):
    """Request for clocking in."""
    work_type: str = Field(default="office", description="Type of work: office, wfh, field")
    latitude: Optional[Decimal] = Field(default=None, description="GPS latitude")
    longitude: Optional[Decimal] = Field(default=None, description="GPS longitude")
    address: Optional[str] = Field(default=None, description="Location address")
    wfh_reason: Optional[str] = Field(default=None, description="Reason for WFH")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class ClockOutRequest(BaseModel):
    """Request for clocking out."""
    latitude: Optional[Decimal] = Field(default=None, description="GPS latitude")
    longitude: Optional[Decimal] = Field(default=None, description="GPS longitude")
    address: Optional[str] = Field(default=None, description="Location address")
    notes: Optional[str] = Field(default=None, description="Additional notes")


class BreakRequest(BaseModel):
    """Request for break start/end."""
    latitude: Optional[Decimal] = Field(default=None, description="GPS latitude")
    longitude: Optional[Decimal] = Field(default=None, description="GPS longitude")


class AttendanceResponse(BaseModel):
    """Attendance record response."""
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    attendance_date: date
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    clock_in_latitude: Optional[Decimal] = None
    clock_in_longitude: Optional[Decimal] = None
    clock_in_address: Optional[str] = None
    clock_out_latitude: Optional[Decimal] = None
    clock_out_longitude: Optional[Decimal] = None
    clock_out_address: Optional[str] = None
    work_type: str
    wfh_reason: Optional[str] = None
    wfh_approved: Optional[bool] = None
    wfh_approved_by: Optional[int] = None
    wfh_approved_at: Optional[datetime] = None
    total_hours: Optional[Decimal] = None
    regular_hours: Optional[Decimal] = None
    overtime_hours: Optional[Decimal] = None
    overtime_type: str
    overtime_approved: Optional[bool] = None
    break_start: Optional[datetime] = None
    break_end: Optional[datetime] = None
    break_duration_minutes: Optional[int] = None
    status: str
    is_late: bool
    late_minutes: Optional[int] = None
    late_reason: Optional[str] = None
    is_early_departure: bool
    early_departure_minutes: Optional[int] = None
    early_departure_reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceSummary(BaseModel):
    """Summary of attendance for a period."""
    employee_id: int
    employee_name: str
    period_start: date
    period_end: date
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    wfh_days: int
    half_days: int
    leave_days: int
    total_hours: Decimal
    regular_hours: Decimal
    overtime_hours: Decimal
    average_clock_in: Optional[str] = None
    average_clock_out: Optional[str] = None


class WFHApprovalRequest(BaseModel):
    """Request to approve/reject WFH."""
    approved: bool
    notes: Optional[str] = None


class OvertimeApprovalRequest(BaseModel):
    """Request to approve/reject overtime."""
    approved: bool
    hours: Optional[Decimal] = None
    notes: Optional[str] = None


class AttendanceFilter(BaseModel):
    """Filter for attendance records."""
    employee_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    work_type: Optional[str] = None
    status: Optional[str] = None
    has_overtime: Optional[bool] = None
    is_wfh: Optional[bool] = None


class TodayAttendanceStatus(BaseModel):
    """Today's attendance status for an employee."""
    date: date
    is_clocked_in: bool
    clock_in_time: Optional[datetime] = None
    is_on_break: bool
    break_start_time: Optional[datetime] = None
    work_type: Optional[str] = None
    can_clock_in: bool
    can_clock_out: bool
    can_start_break: bool
    can_end_break: bool
    message: str


class AttendanceDashboard(BaseModel):
    """Attendance dashboard for admin/HR."""
    total_employees: int
    clocked_in_today: int
    wfh_today: int
    absent_today: int
    late_today: int
    pending_wfh_approvals: int
    pending_overtime_approvals: int
    on_leave_today: int
