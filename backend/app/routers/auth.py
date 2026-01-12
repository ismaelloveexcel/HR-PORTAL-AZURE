from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, status
import jwt
from jwt.exceptions import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.database import get_session
from app.schemas.employee import (
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
)
from app.services.employees import employee_service, create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])


async def get_current_employee_id(authorization: str = Header(...)) -> str:
    """Extract employee ID from JWT token."""
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return employee_id
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def _mask_employee_id(employee_id: str) -> str:
    """
    Mask employee ID for logging to prevent clear-text logging of sensitive information.
    
    This function acts as a sanitizer for PII data, masking the middle characters
    while preserving the first and last 2 characters for debugging purposes.
    
    Args:
        employee_id: The employee ID to mask (sensitive PII)
    
    Returns:
        Masked employee ID safe for logging (sanitized)
    
    Examples:
        >>> _mask_employee_id("BAYN00008")
        'BA***08'
        >>> _mask_employee_id("ABC")
        '***'
    """
    if not employee_id or len(employee_id) < 4:
        return "***"
    # Show first 2 and last 2 characters, mask the middle
    return f"{employee_id[:2]}***{employee_id[-2:]}"


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login with Employee ID and password",
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate with Employee ID and password.
    
    - **First-time login**: Use DOB in DDMMYYYY format as password
    - **Subsequent logins**: Use your custom password
    
    If `requires_password_change` is true, you must change your password.
    """
    settings = get_settings()
    try:
        return await employee_service.login(session, request)
    except HTTPException:
        raise
    except Exception as e:
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        # Mask employee_id if needed for future non-logging use
        masked_id = _mask_employee_id(request.employee_id)
        # Do not log employee IDs (even masked) to avoid exposing sensitive information
        logger.error(f"Login error during authentication: {str(e)}")
        logger.error(f"Login error traceback: {traceback.format_exc()}")
        
        # In development, show actual error
        if settings.app_env == "development":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login error: {str(e)}",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during login. Please check server logs or contact support.",
            )


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change password",
)
async def change_password(
    request: PasswordChangeRequest,
    employee_id: str = Depends(get_current_employee_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Change your password. Requires authentication.
    
    Password requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    success = await employee_service.change_password(session, employee_id, request)
    return {"success": success, "message": "Password changed successfully"}


