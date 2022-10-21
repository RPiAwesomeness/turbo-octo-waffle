from fastapi import FastAPI

from .middleware.custom_header import CustomHeaderMiddleware
from .routers import health


class AmsStatusApp(FastAPI):
    """Class override for AMS-Status-OA"""


# Initialize app. Configuration information could be provided at this point
app = AmsStatusApp()

# Have all endpoints defined via individual routers that are included here
app.include_router(health.router)

# Add all middleware (custom/built-in), passing any necessary arguments
# Order may be important, depending on how security/redirects are handled
app.add_middleware(CustomHeaderMiddleware, header_prefix="Custom")

@app.get("/endpoints")
def list_endpoints():
    return [{"path": route.path, "name": route.name} for route in app.routes]

@app.get("/versions")
def get_versions():
    return [
        {
            "name": 'AMS Status OA',
            "version": "0.0.1-innovate"
        }
    ]

@app.get("/meta")
def get_server_metadata():
    return {
        "endpoints": list_endpoints(),
        "versions": get_versions()
    }

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
