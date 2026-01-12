#!/usr/bin/env python3
"""
Manual verification script for emergency admin recovery endpoints.
This script demonstrates the new functionality without requiring a running server.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_imports():
    """Verify all modules can be imported."""
    print("✓ Testing imports...")
    try:
        from app.routers import auth, health
        from app import main
        print("  ✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def verify_endpoint_signatures():
    """Verify endpoint function signatures."""
    print("\n✓ Testing endpoint signatures...")
    
    try:
        from app.routers import health
        import inspect
        
        # Check health_check_db endpoint
        db_check = health.health_check_db
        sig = inspect.signature(db_check)
        assert 'session' in sig.parameters
        print("  ✓ /api/health/db endpoint signature correct")
        
        # Check reset_admin_password endpoint
        reset_pwd = health.reset_admin_password
        sig = inspect.signature(reset_pwd)
        assert 'secret_token' in sig.parameters
        assert 'session' in sig.parameters
        print("  ✓ /api/health/reset-admin-password endpoint signature correct")
        
        return True
    except Exception as e:
        print(f"  ✗ Signature verification failed: {e}")
        return False


def verify_login_error_handling():
    """Verify login endpoint has enhanced error handling."""
    print("\n✓ Testing login error handling...")
    
    try:
        from app.routers import auth
        import inspect
        
        source = inspect.getsource(auth.login)
        
        # Check for key enhancements
        checks = {
            "traceback module": "import traceback" in source,
            "Employee ID in logs": "employee_id" in source,
            "Environment check": "app_env" in source or "settings.app_env" in source,
            "Development mode error": "development" in source.lower(),
        }
        
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
        
        return all(checks.values())
    except Exception as e:
        print(f"  ✗ Login error handling verification failed: {e}")
        return False


def verify_startup_migration_handling():
    """Verify startup migration has enhanced error handling."""
    print("\n✓ Testing startup migration error handling...")
    
    try:
        from app import main
        import inspect
        
        source = inspect.getsource(main.create_app)
        
        # Check for key enhancements
        checks = {
            "Traceback import": "import traceback" in source,
            "Success logging": "successfully" in source.lower(),
            "Recovery instructions": "reset-admin-password" in source.lower(),
            "Environment-aware": "app_env" in source or "settings.app_env" in source,
        }
        
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
        
        return all(checks.values())
    except Exception as e:
        print(f"  ✗ Startup migration verification failed: {e}")
        return False


def verify_readme_updates():
    """Verify README has emergency recovery section."""
    print("\n✓ Testing README updates...")
    
    try:
        readme_path = Path(__file__).parent.parent.parent / "README.md"
        content = readme_path.read_text()
        
        checks = {
            "Emergency section": "Emergency Admin Password Reset" in content,
            "Reset endpoint example": "reset-admin-password" in content,
            "Health check example": "/api/health/db" in content,
            "Local testing examples": "localhost:8000" in content,
        }
        
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
        
        return all(checks.values())
    except Exception as e:
        print(f"  ✗ README verification failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Emergency Admin Recovery - Manual Verification")
    print("=" * 70)
    
    checks = [
        verify_imports,
        verify_endpoint_signatures,
        verify_login_error_handling,
        verify_startup_migration_handling,
        verify_readme_updates,
    ]
    
    results = [check() for check in checks]
    
    print("\n" + "=" * 70)
    if all(results):
        print("✓ ALL CHECKS PASSED")
        print("=" * 70)
        print("\nNew endpoints available:")
        print("  • GET  /api/health/db - Check database connectivity")
        print("  • POST /api/health/reset-admin-password - Reset admin password")
        print("\nEnhanced error handling:")
        print("  • Login errors now show detailed logs")
        print("  • Startup migrations log tracebacks on failure")
        print("  • Development mode shows actual error messages")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
