#!/usr/bin/env python3
"""
Demo script showing the new emergency recovery endpoints in action.
This simulates the API responses without requiring a running database.
"""

import json
from datetime import datetime


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_request(method, endpoint, headers=None):
    """Print a request."""
    print(f"\n📤 {method} {endpoint}")
    if headers:
        print("   Headers:")
        for key, value in headers.items():
            # Mask secret values
            display_value = "***" if "secret" in key.lower() else value
            print(f"     {key}: {display_value}")


def print_response(status, data):
    """Print a response."""
    status_emoji = "✅" if status < 400 else "❌"
    print(f"\n📥 {status_emoji} Response {status}")
    print(f"   {json.dumps(data, indent=2)}")


def demo_health_db_success():
    """Demo successful database health check."""
    print_section("Database Health Check - Success")
    
    print_request("GET", "/api/health/db")
    
    print_response(200, {
        "database": "connected",
        "employee_count": 42,
        "admin_exists": True,
        "admin_details": {
            "employee_id": "BAYN00008",
            "name": "Ahmed Al Mansoori",
            "role": "admin",
            "is_active": True
        }
    })
    
    print("\n💡 Interpretation:")
    print("   • Database is connected")
    print("   • 42 employees in database")
    print("   • Admin account exists and is active")
    print("   • Ready for use")


def demo_health_db_failure():
    """Demo failed database health check."""
    print_section("Database Health Check - Connection Failed")
    
    print_request("GET", "/api/health/db")
    
    print_response(503, {
        "detail": "Database connection failed: connection refused"
    })
    
    print("\n💡 Interpretation:")
    print("   • Database is not accessible")
    print("   • Check database server is running")
    print("   • Check connection string in environment")


def demo_reset_password_success():
    """Demo successful password reset."""
    print_section("Admin Password Reset - Success")
    
    print_request(
        "POST",
        "/api/health/reset-admin-password",
        {"X-Admin-Secret": "your-secret-key"}
    )
    
    print_response(200, {
        "success": True,
        "message": "Password reset for BAYN00008 - Ahmed Al Mansoori",
        "employee_id": "BAYN00008",
        "name": "Ahmed Al Mansoori",
        "role": "admin",
        "is_active": True
    })
    
    print("\n💡 Next Steps:")
    print("   1. Login with employee_id: BAYN00008")
    print("   2. Use password: 16051988 (admin's date of birth)")
    print("   3. System will prompt to change password")
    print("   4. Set a new secure password")
    print("\n💡 Security Note:")
    print("   • Password only shown in response in development mode")
    print("   • Production mode omits password for security")
    print("   • Password is always: 16051988 (DOB format: DDMMYYYY)")


def demo_reset_password_forbidden():
    """Demo password reset with wrong token."""
    print_section("Admin Password Reset - Wrong Token")
    
    print_request(
        "POST",
        "/api/health/reset-admin-password",
        {"X-Admin-Secret": "wrong-token"}
    )
    
    print_response(403, {
        "detail": "Invalid secret token"
    })
    
    print("\n💡 Interpretation:")
    print("   • Secret token doesn't match AUTH_SECRET_KEY")
    print("   • Check your environment variables")
    print("   • This attempt was logged for security")


def demo_login_error_development():
    """Demo login error in development mode."""
    print_section("Login Error - Development Mode")
    
    print_request(
        "POST",
        "/api/auth/login",
        {"Content-Type": "application/json"}
    )
    
    print("   Body:")
    print("   {")
    print('     "employee_id": "BAYN00008",')
    print('     "password": "wrong-password"')
    print("   }")
    
    print_response(500, {
        "detail": "Login error: Invalid password"
    })
    
    print("\n💡 Development Mode Features:")
    print("   • Actual error message returned")
    print("   • Full traceback in server logs")
    print("   • Employee ID included in logs")
    print("   • Helps with debugging")


def demo_login_error_production():
    """Demo login error in production mode."""
    print_section("Login Error - Production Mode")
    
    print_request(
        "POST",
        "/api/auth/login",
        {"Content-Type": "application/json"}
    )
    
    print("   Body:")
    print("   {")
    print('     "employee_id": "BAYN00008",')
    print('     "password": "wrong-password"')
    print("   }")
    
    print_response(500, {
        "detail": "An error occurred during login. Please check server logs or contact support."
    })
    
    print("\n💡 Production Mode Features:")
    print("   • Generic error message to users")
    print("   • Detailed error in server logs")
    print("   • Full traceback in server logs")
    print("   • Employee ID in logs for support")


def demo_startup_migration_logs():
    """Demo startup migration logs."""
    print_section("Startup Migration Logs")
    
    print("\n✅ Success Scenario:")
    print("   INFO Application startup")
    print("   INFO Startup migrations completed successfully")
    
    print("\n❌ Failure Scenario (Development):")
    print("   ERROR Startup migrations failed: relation 'employees' does not exist")
    print("   ERROR Startup migration traceback: Traceback (most recent call last)...")
    print("   WARNING Startup migration failed in development mode")
    
    print("\n❌ Failure Scenario (Production):")
    print("   ERROR Startup migrations failed: relation 'employees' does not exist")
    print("   ERROR Startup migration traceback: Traceback (most recent call last)...")
    print("   ERROR Startup migration failed in production - use /api/health/reset-admin-password to recover")
    
    print("\n💡 Features:")
    print("   • Clear success/failure indication")
    print("   • Full traceback for debugging")
    print("   • Recovery instructions in logs")
    print("   • Environment-aware messaging")


def print_usage_examples():
    """Print real-world usage examples."""
    print_section("Real-World Usage Examples")
    
    print("\n🔧 Example 1: Check if system is healthy")
    print("   $ curl http://localhost:8000/api/health/db")
    
    print("\n🔧 Example 2: Reset admin password (development)")
    print("   $ curl -X POST http://localhost:8000/api/health/reset-admin-password \\")
    print('     -H "X-Admin-Secret: dev-secret-key-change-in-production"')
    
    print("\n🔧 Example 3: Reset admin password (production)")
    print("   $ curl -X POST https://hr-portal.company.com/api/health/reset-admin-password \\")
    print('     -H "X-Admin-Secret: $(cat /secure/auth_secret_key)"')
    
    print("\n🔧 Example 4: Check health and reset if needed (bash)")
    print("   $ if curl -s http://localhost:8000/api/health/db | grep -q 'connected'; then")
    print("       echo 'Database OK'")
    print("     else")
    print("       echo 'Database issue - attempting admin reset'")
    print('       curl -X POST http://localhost:8000/api/health/reset-admin-password \\')
    print('         -H "X-Admin-Secret: $AUTH_SECRET_KEY"')
    print("     fi")


def main():
    """Run all demos."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Emergency Admin Recovery - API Demo" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    
    demos = [
        demo_health_db_success,
        demo_health_db_failure,
        demo_reset_password_success,
        demo_reset_password_forbidden,
        demo_login_error_development,
        demo_login_error_production,
        demo_startup_migration_logs,
        print_usage_examples,
    ]
    
    for demo in demos:
        demo()
    
    print("\n" + "=" * 70)
    print("  For more information, see:")
    print("  • docs/EMERGENCY_RECOVERY_GUIDE.md")
    print("  • README.md (Emergency Admin Password Reset section)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
