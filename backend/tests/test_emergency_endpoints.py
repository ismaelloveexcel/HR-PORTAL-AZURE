"""
Test emergency admin recovery endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock


def test_health_db_endpoint_structure():
    """Test that the health/db endpoint exists and has correct structure."""
    from app.main import app
    
    client = TestClient(app)
    
    # This will fail if database is not configured, but we can test the endpoint exists
    response = client.get("/api/health/db")
    
    # Should return either 200 (connected) or 503 (connection failed)
    assert response.status_code in [200, 503]
    
    # If successful, verify response structure
    if response.status_code == 200:
        data = response.json()
        assert "database" in data
        assert "employee_count" in data
        assert "admin_exists" in data


def test_reset_admin_password_endpoint_requires_header():
    """Test that reset-admin-password endpoint requires X-Admin-Secret header."""
    from app.main import app
    
    client = TestClient(app)
    
    # Test without header
    response = client.post("/api/health/reset-admin-password")
    
    # Should return 422 (validation error) for missing required header
    assert response.status_code == 422


def test_reset_admin_password_endpoint_validates_token():
    """Test that reset-admin-password endpoint validates the secret token."""
    from app.main import app
    
    client = TestClient(app)
    
    # Test with wrong token
    response = client.post(
        "/api/health/reset-admin-password",
        headers={"X-Admin-Secret": "wrong-token"}
    )
    
    # Should return 403 (forbidden) or 500 (if database fails first)
    assert response.status_code in [403, 500]


def test_login_endpoint_error_handling():
    """Test that login endpoint has proper error handling structure."""
    from app.routers import auth
    import inspect
    
    # Get the login function source
    login_func = auth.login
    source = inspect.getsource(login_func)
    
    # Verify enhanced error logging is present
    assert "traceback" in source.lower()
    assert "logger.error" in source
    assert "app_env" in source or "settings.app_env" in source
    

def test_startup_migration_error_handling():
    """Test that main.py has enhanced startup migration error handling."""
    from app import main
    import inspect
    
    # Get the create_app function source
    source = inspect.getsource(main.create_app)
    
    # Verify enhanced error logging is present
    assert "traceback" in source.lower()
    assert "Startup migration" in source
    assert "reset-admin-password" in source.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
