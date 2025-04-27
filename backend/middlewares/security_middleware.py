from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)

        # Security Headers
        response.headers["X-Frame-Options"] = "DENY"  # Prevent Clickjacking
        response.headers["X-Content-Type-Options"] = "nosniff"  # Prevent MIME sniffing
        response.headers["X-XSS-Protection"] = "1; mode=block"  # Prevent XSS attacks
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"  # Enforce HTTPS

        return response
