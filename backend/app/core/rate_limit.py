"""Rate limiting configuration for the application."""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a single limiter instance to be used across the application
# This avoids circular imports when routers need access to the limiter
limiter = Limiter(key_func=get_remote_address)
