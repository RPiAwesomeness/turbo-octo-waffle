"""An example middle that just adds a simple header to request and response objects"""
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_prefix: str="Custom") -> None:
        super().__init__(app)
        self.header_prefix = header_prefix

    async def dispatch(self, request, call_next):
        # Pass reques on to the next middleware in the stack
        response = await call_next(request)

        # Response headers can be directly manipulated
        response.headers[f"X-{self.header_prefix}-Response-Header"] = f"Added After Handlers @ {datetime.utcnow()}"
        return response
