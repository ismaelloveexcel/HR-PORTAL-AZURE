"""
Test to verify that sensitive information is properly masked in logs.
This addresses the CodeQL security vulnerabilities.
"""
import pytest
from app.routers.auth import _mask_employee_id
from app.routers.health import _mask_employee_id as health_mask_employee_id


def test_mask_employee_id_auth():
    """Test that employee IDs are properly masked in auth router."""
    # Test standard employee ID
    assert _mask_employee_id("BAYN00008") == "BA***08"
    
    # Test shorter IDs
    assert _mask_employee_id("EMP001") == "EM***01"
    
    # Test very short IDs
    assert _mask_employee_id("ABC") == "***"
    
    # Test longer IDs
    assert _mask_employee_id("EMPLOYEE123") == "EM***23"


def test_mask_employee_id_health():
    """Test that employee IDs are properly masked in health router."""
    # Test standard employee ID
    assert health_mask_employee_id("BAYN00008") == "BA***08"
    
    # Test admin ID
    assert health_mask_employee_id("ADMIN001") == "AD***01"


def test_mask_employee_id_edge_cases():
    """Test edge cases for employee ID masking."""
    # Empty string
    assert _mask_employee_id("") == "***"
    
    # Single character
    assert _mask_employee_id("A") == "***"
    
    # Two characters
    assert _mask_employee_id("AB") == "***"
    
    # Three characters
    assert _mask_employee_id("ABC") == "***"
    
    # Four characters (minimum for pattern)
    assert _mask_employee_id("ABCD") == "AB***CD"


def test_masking_prevents_pii_exposure():
    """Verify that masking effectively prevents PII exposure."""
    original = "BAYN00008"
    masked = _mask_employee_id(original)
    
    # Masked version should not contain the full original
    assert original != masked
    
    # Masked version should contain stars
    assert "***" in masked
    
    # Masked version should be shorter or equal length
    assert len(masked) <= len(original) + 3  # accounting for ***
    
    # First and last 2 characters should be preserved for debugging
    if len(original) >= 4:
        assert masked.startswith(original[:2])
        assert masked.endswith(original[-2:])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
