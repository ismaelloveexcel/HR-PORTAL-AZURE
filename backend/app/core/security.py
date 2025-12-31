from typing import List, Optional

from app.auth.dependencies import require_role as _require_role


def sanitize_text(value: str) -> str:
    """Basic input sanitization to avoid script injection."""
    import html

    return html.escape(value.strip())


def require_role(allowed: Optional[List[str]] = None):
    return _require_role(allowed)
