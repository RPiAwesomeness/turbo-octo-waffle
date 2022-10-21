from http import client
import json
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .middleware.custom_header import CustomHeaderMiddleware
from .routers import health, test
from .handlers import json_decode, file_read, request_validation_handler


class AmsStatusApp(FastAPI):
    """Class override for AMS-Status-OA"""


# Initialize app. Configuration information could be provided at this point
app = AmsStatusApp()

# Have all endpoints defined via individual routers that are included here
app.include_router(health.router, tags=["Service Status"])
app.include_router(test.router, tags=["FastAPI Testing"])

# Add all middleware (custom/built-in), passing any necessary arguments
# Order may be important, depending on how security/redirects are handled
app.add_middleware(CustomHeaderMiddleware, header_prefix="Custom")

# Add custom exception handlers
app.add_exception_handler(json.JSONDecodeError, json_decode.handler)
app.add_exception_handler(client.IncompleteRead, file_read.handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)

@app.get("/endpoints", tags=["Server Meta"])
def list_endpoints():
    return [
        {
            "name": getattr(route, "name", "Unknown route name"),
            "path": getattr(route, "path", "Unknown route path"),
        } for route in app.routes
    ]

@app.get("/versions", tags=["Server Meta"])
def get_versions():
    return [
        {
            "name": 'AMS Status OA',
            "version": "0.0.1-innovate"
        }
    ]

@app.get("/meta", tags=["Server Meta"])
def get_server_metadata():
    return {
        "endpoints": list_endpoints(),
        "versions": get_versions()
    }

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
