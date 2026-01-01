from typing import List, Optional

<<<<<<< HEAD
from app.auth.dependencies import require_role as _require_role
=======
from fastapi import Header, HTTPException, status

ALLOWED_ROLES = {"admin", "hr", "viewer"}
>>>>>>> origin/codex/add-database-and-audit-layer-to-secure-renewals


def sanitize_text(value: str) -> str:
    """Basic input sanitization to avoid script injection."""
    import html

    return html.escape(value.strip())


def require_role(allowed: Optional[List[str]] = None):
<<<<<<< HEAD
    return _require_role(allowed)
=======
    async def dependency(x_role: str | None = Header(default=None, alias="X-Role")) -> str:
        if x_role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Role header missing")

        role = x_role.strip().lower()
        if role not in ALLOWED_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")
        if allowed and role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return role

    return dependency
>>>>>>> origin/codex/add-database-and-audit-layer-to-secure-renewals
