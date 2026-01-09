"""Leave management router."""
from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
import jwt
from jwt.exceptions import PyJWTError
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.database import get_session
from app.models.employee import Employee
from app.models.leave import LeaveRequest, LeaveBalance, LEAVE_TYPES, LEAVE_STATUSES
from app.schemas.leave import (
    LeaveBalanceResponse, LeaveBalanceSummary, LeaveRequestCreate,
    LeaveRequestResponse, LeaveApprovalRequest, LeaveCalendarEntry
)

router = APIRouter(prefix="/leave", tags=["Leave Management"])


async def get_current_employee(
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_session)
) -> Employee:
    """Extract and validate employee from JWT token."""
    try:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header",
            )
        settings = get_settings()
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=["HS256"])
        employee_id = payload.get("sub")
        if not employee_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        result = await session.execute(
            select(Employee).where(Employee.id == int(employee_id))
        )
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")


@router.get("/types")
async def get_leave_types():
    """Get list of available leave types."""
    return {
        "leave_types": LEAVE_TYPES,
        "descriptions": {
            "annual": "Annual leave per Article 29",
            "sick": "Sick leave per Article 31",
            "maternity": "Maternity leave per Article 30",
            "paternity": "Paternity leave",
            "compassionate": "Bereavement/compassionate leave",
            "hajj": "Hajj leave (once during employment)",
            "unpaid": "Unpaid leave",
            "study": "Study leave",
            "marriage": "Marriage leave",
            "emergency": "Emergency leave"
        }
    }


@router.get("/balance/{employee_id}", response_model=LeaveBalanceSummary)
async def get_leave_balance(
    employee_id: int,
    year: int = Query(default=None, description="Year (defaults to current year)"),
    current_user: Employee = Depends(get_current_employee),
    session: AsyncSession = Depends(get_session)
):
    """Get leave balance summary for an employee."""
    if current_user.role not in ["admin", "hr"] and current_user.id != employee_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not year:
        year = date.today().year
    
    # Get employee
    emp_result = await session.execute(
        select(Employee).where(Employee.id == employee_id)
    )
    employee = emp_result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get balances
    result = await session.execute(
        select(LeaveBalance).where(
            and_(
                LeaveBalance.employee_id == employee_id,
                LeaveBalance.year == year
            )
        )
    )
    balances = result.scalars().all()
    
    return LeaveBalanceSummary(
        employee_id=employee_id,
        employee_name=employee.name,
        year=year,
        balances=[
            LeaveBalanceResponse(
                id=b.id,
                employee_id=b.employee_id,
                year=b.year,
                leave_type=b.leave_type,
                entitlement=b.entitlement,
                carried_forward=b.carried_forward,
                used=b.used,
                pending=b.pending,
                adjustment=b.adjustment,
                adjustment_reason=b.adjustment_reason,
                available=b.available
            )
            for b in balances
        ]
    )


@router.post("/request", response_model=LeaveRequestResponse)
async def create_leave_request(
    request: LeaveRequestCreate,
    current_user: Employee = Depends(get_current_employee),
    session: AsyncSession = Depends(get_session)
):
    """Create a new leave request."""
    from decimal import Decimal
    
    if request.leave_type not in LEAVE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid leave type. Must be one of: {LEAVE_TYPES}")
    
    if request.end_date < request.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    # Check for overlapping requests
    existing = await session.execute(
        select(LeaveRequest).where(
            and_(
                LeaveRequest.employee_id == current_user.id,
                LeaveRequest.status.in_(["pending", "approved"]),
                LeaveRequest.start_date <= request.end_date,
                LeaveRequest.end_date >= request.start_date
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Overlapping leave request already exists")
    
    # Calculate days
    if request.is_half_day:
        total_days = Decimal("0.5")
    else:
        delta = (request.end_date - request.start_date).days + 1
        total_days = Decimal(str(delta))
    
    leave_request = LeaveRequest(
        employee_id=current_user.id,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        is_half_day=request.is_half_day,
        half_day_type=request.half_day_type,
        total_days=total_days,
        reason=request.reason,
        emergency_contact=request.emergency_contact,
        emergency_phone=request.emergency_phone,
        status="pending"
    )
    
    session.add(leave_request)
    await session.commit()
    await session.refresh(leave_request)
    
    return LeaveRequestResponse(
        id=leave_request.id,
        employee_id=leave_request.employee_id,
        employee_name=current_user.name,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        is_half_day=leave_request.is_half_day,
        half_day_type=leave_request.half_day_type,
        total_days=leave_request.total_days,
        reason=leave_request.reason,
        status=leave_request.status,
        created_at=leave_request.created_at
    )


@router.get("/requests", response_model=List[LeaveRequestResponse])
async def get_leave_requests(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    current_user: Employee = Depends(get_current_employee),
    session: AsyncSession = Depends(get_session)
):
    """Get leave requests for current user or all (for HR/admin)."""
    query = select(LeaveRequest)
    
    if current_user.role not in ["admin", "hr"]:
        query = query.where(LeaveRequest.employee_id == current_user.id)
    
    if status_filter:
        query = query.where(LeaveRequest.status == status_filter)
    
    query = query.order_by(LeaveRequest.created_at.desc())
    
    result = await session.execute(query)
    requests = result.scalars().all()
    
    return [
        LeaveRequestResponse(
            id=r.id,
            employee_id=r.employee_id,
            leave_type=r.leave_type,
            start_date=r.start_date,
            end_date=r.end_date,
            is_half_day=r.is_half_day,
            half_day_type=r.half_day_type,
            total_days=r.total_days,
            reason=r.reason,
            document_url=r.document_url,
            status=r.status,
            approved_by=r.approved_by,
            approved_at=r.approved_at,
            rejection_reason=r.rejection_reason,
            emergency_contact=r.emergency_contact,
            emergency_phone=r.emergency_phone,
            created_at=r.created_at
        )
        for r in requests
    ]


@router.post("/{request_id}/approve", response_model=LeaveRequestResponse)
async def approve_leave_request(
    request_id: int,
    approval: LeaveApprovalRequest,
    current_user: Employee = Depends(get_current_employee),
    session: AsyncSession = Depends(get_session)
):
    """Approve or reject a leave request (manager/HR only)."""
    if current_user.role not in ["admin", "hr", "manager"]:
        raise HTTPException(status_code=403, detail="Only managers and HR can approve leave")
    
    result = await session.execute(
        select(LeaveRequest).where(LeaveRequest.id == request_id)
    )
    leave_request = result.scalar_one_or_none()
    
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    if leave_request.status != "pending":
        raise HTTPException(status_code=400, detail="Leave request is not pending")
    
    # For managers, verify they manage this employee
    if current_user.role == "manager":
        emp_result = await session.execute(
            select(Employee).where(Employee.id == leave_request.employee_id)
        )
        employee = emp_result.scalar_one_or_none()
        if not employee or employee.line_manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only approve leave for your direct reports")
    
    now = datetime.now(timezone.utc)
    
    if approval.approved:
        leave_request.status = "approved"
        leave_request.approved_by = current_user.id
        leave_request.approved_at = now
        
        # Update leave balance
        balance_result = await session.execute(
            select(LeaveBalance).where(
                and_(
                    LeaveBalance.employee_id == leave_request.employee_id,
                    LeaveBalance.year == leave_request.start_date.year,
                    LeaveBalance.leave_type == leave_request.leave_type
                )
            )
        )
        balance = balance_result.scalar_one_or_none()
        if balance:
            balance.pending += leave_request.total_days
    else:
        leave_request.status = "rejected"
        leave_request.rejection_reason = approval.rejection_reason
    
    await session.commit()
    await session.refresh(leave_request)
    
    return LeaveRequestResponse(
        id=leave_request.id,
        employee_id=leave_request.employee_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        is_half_day=leave_request.is_half_day,
        half_day_type=leave_request.half_day_type,
        total_days=leave_request.total_days,
        reason=leave_request.reason,
        status=leave_request.status,
        approved_by=leave_request.approved_by,
        approved_at=leave_request.approved_at,
        rejection_reason=leave_request.rejection_reason,
        created_at=leave_request.created_at
    )


@router.get("/calendar", response_model=List[LeaveCalendarEntry])
async def get_leave_calendar(
    start_date: date = Query(..., description="Calendar start date"),
    end_date: date = Query(..., description="Calendar end date"),
    current_user: Employee = Depends(get_current_employee),
    session: AsyncSession = Depends(get_session)
):
    """Get leave calendar for a date range (approved leaves only)."""
    result = await session.execute(
        select(LeaveRequest, Employee).join(
            Employee, LeaveRequest.employee_id == Employee.id
        ).where(
            and_(
                LeaveRequest.status == "approved",
                LeaveRequest.start_date <= end_date,
                LeaveRequest.end_date >= start_date
            )
        ).order_by(LeaveRequest.start_date)
    )
    leaves = result.all()
    
    return [
        LeaveCalendarEntry(
            employee_id=leave.employee_id,
            employee_name=emp.name,
            leave_type=leave.leave_type,
            start_date=leave.start_date,
            end_date=leave.end_date,
            status=leave.status,
            is_half_day=leave.is_half_day
        )
        for leave, emp in leaves
    ]
