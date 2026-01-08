"""Census Verification API endpoints for employee self-service."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets

from app.database import get_session
from app.auth.dependencies import require_role
from app.models import (
    CensusVerificationToken, InsuranceCensusRecord, Employee,
    DHA_DOH_VALIDATION_FIELDS, AMENDMENT_TRACKED_FIELDS
)

router = APIRouter(
    prefix="/census-verification",
    tags=["census-verification"],
)


# ============== Pydantic Models ==============

class CensusVerificationData(BaseModel):
    """Data returned for employee verification page."""
    token: str
    employee_name: str
    staff_id: str
    entity: str
    insurance_type: str
    # Current data
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    family_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    marital_status: Optional[str] = None
    emirates_id_number: Optional[str] = None
    uid_number: Optional[str] = None
    gdrfa_file_number: Optional[str] = None
    passport_number: Optional[str] = None
    mobile_no: Optional[str] = None
    personal_email: Optional[str] = None
    # Missing fields
    dha_doh_missing_fields: List[str] = []
    missing_fields: List[str] = []
    # Status
    already_verified: bool = False


class CensusUpdateSubmit(BaseModel):
    """Data submitted by employee."""
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    family_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    marital_status: Optional[str] = None
    emirates_id_number: Optional[str] = None
    uid_number: Optional[str] = None
    gdrfa_file_number: Optional[str] = None
    passport_number: Optional[str] = None
    mobile_no: Optional[str] = None
    personal_email: Optional[str] = None
    confirmed: bool = False


class SendEmailsRequest(BaseModel):
    """Request to send verification emails."""
    entity: Optional[str] = None  # Filter by entity
    insurance_type: Optional[str] = None  # Filter by insurance type
    missing_fields_only: bool = True  # Only send to those with missing DHA/DOH fields
    expires_in_days: int = 14


class VerificationStats(BaseModel):
    """Statistics for verification campaign."""
    total_tokens: int
    emails_sent: int
    verified: int
    pending: int
    expired: int


# ============== Public Endpoints (Token-based) ==============

@router.get(
    "/validate/{token}",
    summary="Validate verification token",
)
async def validate_token(
    token: str,
    db: AsyncSession = Depends(get_session),
):
    """Validate a census verification token. Public endpoint."""
    result = await db.execute(
        select(CensusVerificationToken).where(CensusVerificationToken.token == token)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        return {"valid": False, "message": "Invalid verification link"}
    
    if verification.is_expired or verification.expires_at < datetime.utcnow():
        return {"valid": False, "message": "This verification link has expired"}
    
    if verification.verified:
        return {"valid": True, "message": "Already verified", "already_verified": True}
    
    return {"valid": True, "message": "Token is valid"}


@router.get(
    "/data/{token}",
    response_model=CensusVerificationData,
    summary="Get census data for verification",
)
async def get_verification_data(
    token: str,
    db: AsyncSession = Depends(get_session),
):
    """Get employee's census data for verification. Public endpoint."""
    result = await db.execute(
        select(CensusVerificationToken)
        .options(selectinload(CensusVerificationToken.census_record))
        .where(CensusVerificationToken.token == token)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Invalid verification link")
    
    if verification.is_expired or verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="This verification link has expired")
    
    record = verification.census_record
    if not record:
        raise HTTPException(status_code=404, detail="Census record not found")
    
    return CensusVerificationData(
        token=token,
        employee_name=record.full_name or f"{record.first_name or ''} {record.family_name or ''}".strip() or "Employee",
        staff_id=record.staff_id or "",
        entity=record.entity,
        insurance_type=record.insurance_type,
        full_name=record.full_name,
        first_name=record.first_name,
        second_name=record.second_name,
        family_name=record.family_name,
        dob=record.dob,
        gender=record.gender,
        nationality=record.nationality,
        marital_status=record.marital_status,
        emirates_id_number=record.emirates_id_number,
        uid_number=record.uid_number,
        gdrfa_file_number=record.gdrfa_file_number,
        passport_number=record.passport_number,
        mobile_no=record.mobile_no,
        personal_email=record.personal_email,
        dha_doh_missing_fields=record.dha_doh_missing_fields or [],
        missing_fields=record.missing_fields or [],
        already_verified=verification.verified,
    )


@router.post(
    "/submit/{token}",
    summary="Submit census updates",
)
async def submit_verification(
    token: str,
    data: CensusUpdateSubmit,
    db: AsyncSession = Depends(get_session),
):
    """Submit census data updates. Public endpoint."""
    if not data.confirmed:
        raise HTTPException(status_code=400, detail="Please confirm the information is correct")
    
    result = await db.execute(
        select(CensusVerificationToken)
        .options(selectinload(CensusVerificationToken.census_record))
        .where(CensusVerificationToken.token == token)
    )
    verification = result.scalar_one_or_none()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Invalid verification link")
    
    if verification.is_expired or verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="This verification link has expired")
    
    record = verification.census_record
    if not record:
        raise HTTPException(status_code=404, detail="Census record not found")
    
    # Track amendments
    update_data = data.model_dump(exclude={'confirmed'}, exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            old_value = getattr(record, field, None)
            if old_value != value and field in AMENDMENT_TRACKED_FIELDS:
                record.mark_field_as_amended(field)
            setattr(record, field, value)
    
    # Recalculate completeness
    record.calculate_completeness()
    # Enhanced audit trail with employee/record identifiers
    record.updated_by = f"employee_self_verification_token_{verification.id}_record_{record.id}"
    record.updated_at = datetime.utcnow()
    
    # Mark token as verified
    verification.verified = True
    verification.verified_at = datetime.utcnow()
    verification.updates_submitted = True
    verification.is_used = True
    
    await db.commit()
    
    return {
        "success": True,
        "message": "Your insurance details have been updated successfully. Thank you for verifying your information."
    }


# ============== Protected Endpoints (HR/Admin) ==============

@router.post(
    "/generate-tokens",
    summary="Generate verification tokens for census records",
    dependencies=[Depends(require_role(["admin", "hr"]))],
)
async def generate_tokens(
    request: Request,
    data: SendEmailsRequest,
    db: AsyncSession = Depends(get_session),
    created_by: str = Query("hr"),
):
    """Generate verification tokens for census records. HR/Admin only."""
    query = select(InsuranceCensusRecord).where(InsuranceCensusRecord.relation == 'employee')
    
    if data.entity:
        query = query.where(InsuranceCensusRecord.entity == data.entity)
    if data.insurance_type:
        query = query.where(InsuranceCensusRecord.insurance_type == data.insurance_type)
    if data.missing_fields_only:
        query = query.where(InsuranceCensusRecord.dha_doh_valid == False)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    base_url = str(request.base_url).rstrip("/")
    tokens_created = 0
    
    for record in records:
        # Check if active token already exists
        existing = await db.execute(
            select(CensusVerificationToken).where(
                and_(
                    CensusVerificationToken.census_record_id == record.id,
                    CensusVerificationToken.is_expired == False,
                    CensusVerificationToken.verified == False,
                    CensusVerificationToken.expires_at > datetime.utcnow()
                )
            )
        )
        if existing.scalar_one_or_none():
            continue  # Skip - active token exists
        
        # Generate unique token (64 bytes for enhanced security)
        token = secrets.token_urlsafe(64)
        
        # Get email from linked employee or census record
        email = record.personal_email
        if record.employee_id:
            emp_result = await db.execute(
                select(Employee).where(Employee.id == record.employee_id)
            )
            emp = emp_result.scalar_one_or_none()
            if emp and emp.email:
                email = emp.email
        
        verification = CensusVerificationToken(
            token=token,
            census_record_id=record.id,
            employee_id=record.employee_id,
            email_address=email,
            expires_at=datetime.utcnow() + timedelta(days=data.expires_in_days),
            created_by=created_by,
        )
        db.add(verification)
        tokens_created += 1
    
    await db.commit()
    
    return {
        "success": True,
        "tokens_created": tokens_created,
        "message": f"Generated {tokens_created} verification tokens",
        "verification_url_format": f"{base_url}/verify-census/{{token}}"
    }


@router.get(
    "/tokens",
    summary="List all verification tokens",
    dependencies=[Depends(require_role(["admin", "hr"]))],
)
async def list_tokens(
    db: AsyncSession = Depends(get_session),
    entity: Optional[str] = Query(None),
    verified: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """List verification tokens with status. HR/Admin only."""
    query = select(CensusVerificationToken).options(
        selectinload(CensusVerificationToken.census_record)
    )
    
    if verified is not None:
        query = query.where(CensusVerificationToken.verified == verified)
    
    # Get total
    count_query = select(func.count()).select_from(CensusVerificationToken)
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0
    
    # Paginate
    query = query.order_by(CensusVerificationToken.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    tokens = result.scalars().all()
    
    return {
        "tokens": [
            {
                **t.to_dict(),
                "employee_name": t.census_record.full_name if t.census_record else None,
                "staff_id": t.census_record.staff_id if t.census_record else None,
                "entity": t.census_record.entity if t.census_record else None,
            }
            for t in tokens
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get(
    "/stats",
    response_model=VerificationStats,
    summary="Get verification statistics",
    dependencies=[Depends(require_role(["admin", "hr"]))],
)
async def get_stats(
    db: AsyncSession = Depends(get_session),
):
    """Get verification campaign statistics. HR/Admin only."""
    # Total tokens
    total_result = await db.execute(
        select(func.count()).select_from(CensusVerificationToken)
    )
    total = total_result.scalar() or 0
    
    # Emails sent
    sent_result = await db.execute(
        select(func.count()).select_from(CensusVerificationToken)
        .where(CensusVerificationToken.email_sent == True)
    )
    emails_sent = sent_result.scalar() or 0
    
    # Verified
    verified_result = await db.execute(
        select(func.count()).select_from(CensusVerificationToken)
        .where(CensusVerificationToken.verified == True)
    )
    verified = verified_result.scalar() or 0
    
    # Expired
    expired_result = await db.execute(
        select(func.count()).select_from(CensusVerificationToken)
        .where(
            CensusVerificationToken.is_expired == True
        )
    )
    expired = expired_result.scalar() or 0
    
    return VerificationStats(
        total_tokens=total,
        emails_sent=emails_sent,
        verified=verified,
        pending=total - verified - expired,
        expired=expired,
    )


@router.post(
    "/send-emails",
    summary="Send verification emails",
    dependencies=[Depends(require_role(["admin", "hr"]))],
)
async def send_verification_emails(
    request: Request,
    db: AsyncSession = Depends(get_session),
    limit: int = Query(50, description="Max emails to send"),
):
    """
    Send verification emails to employees with pending tokens.
    HR/Admin only.
    
    Note: Requires SMTP configuration to be set up.
    For now, returns the email content that would be sent.
    """
    base_url = str(request.base_url).rstrip("/")
    
    # Get unsent tokens
    result = await db.execute(
        select(CensusVerificationToken)
        .options(selectinload(CensusVerificationToken.census_record))
        .where(
            and_(
                CensusVerificationToken.email_sent == False,
                CensusVerificationToken.is_expired == False,
                CensusVerificationToken.expires_at > datetime.utcnow()
            )
        )
        .limit(limit)
    )
    tokens = result.scalars().all()
    
    emails_to_send = []
    for token in tokens:
        if not token.email_address:
            continue
        
        record = token.census_record
        employee_name = record.full_name if record else "Employee"
        verification_url = f"{base_url}/verify-census/{token.token}"
        
        # Email template matching pass design
        email_content = {
            "to": token.email_address,
            "subject": "🏥 Action Required: Verify Your Insurance Details",
            "body": f"""
Dear {employee_name},

We are preparing for the upcoming Medical Insurance Renewal and need you to verify your details.

🔗 **Click here to verify your information:**
{verification_url}

**What you need to do:**
1. Click the link above
2. Review your current information
3. Fill in any missing details (highlighted in red)
4. Confirm your information is correct

**Important Fields Required:**
- Emirates ID Number
- Passport Number
- Visa File Number (GDRFA)
- UID Number
- Date of Birth
- Nationality
- Gender

⚠️ **This link expires in 14 days.**

If you have any questions, please contact HR.

Best regards,
HR Department
Baynunah Group
            """.strip(),
            "verification_url": verification_url,
        }
        emails_to_send.append(email_content)
        
        # Mark as sent (in a real implementation, this would happen after actual email send)
        token.email_sent = True
        token.email_sent_at = datetime.utcnow()
    
    await db.commit()
    
    return {
        "success": True,
        "emails_prepared": len(emails_to_send),
        "message": f"Prepared {len(emails_to_send)} verification emails",
        "emails": emails_to_send,  # For testing - shows what would be sent
        "note": "SMTP integration pending - emails shown for preview"
    }


@router.post(
    "/send-reminders",
    summary="Send reminder emails",
    dependencies=[Depends(require_role(["admin", "hr"]))],
)
async def send_reminders(
    request: Request,
    db: AsyncSession = Depends(get_session),
    limit: int = Query(50),
):
    """Send reminder emails to non-responders. HR/Admin only."""
    base_url = str(request.base_url).rstrip("/")
    
    # Get tokens where email was sent but not verified
    result = await db.execute(
        select(CensusVerificationToken)
        .options(selectinload(CensusVerificationToken.census_record))
        .where(
            and_(
                CensusVerificationToken.email_sent == True,
                CensusVerificationToken.verified == False,
                CensusVerificationToken.is_expired == False,
                CensusVerificationToken.expires_at > datetime.utcnow(),
                CensusVerificationToken.reminder_count < 3  # Max 3 reminders
            )
        )
        .limit(limit)
    )
    tokens = result.scalars().all()
    
    reminders_sent = 0
    for token in tokens:
        if not token.email_address:
            continue
        
        token.reminder_count += 1
        token.last_reminder_at = datetime.utcnow()
        reminders_sent += 1
    
    await db.commit()
    
    return {
        "success": True,
        "reminders_sent": reminders_sent,
        "message": f"Sent {reminders_sent} reminder emails"
    }
