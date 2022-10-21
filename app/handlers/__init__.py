from typing import Optional
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def build_response(err_type: str, message: str, status_code: int = 400, **kwargs):
    # Have to return specific Response object in handlers with status code
    return JSONResponse(
        content={
            "error": {
                "type": err_type,
                "message": message,
                "code": status_code,
                **kwargs
            }
        },
        status_code=status_code
    )

def build_exc_response(err_type: str, ex: Exception, message: Optional[str] = None, **kwargs):
    return build_response(err_type, message if message is not None else getattr(ex, "msg", "Unknown Error"), **kwargs)
    
def map_to_error_obj(ex):
    return (".".join(ex["loc"][1:]), ex["msg"])

def request_validation_handler(_request: Request, err: RequestValidationError):
    """Maps FastAPI errors to match other errors"""
    headers = map(
        map_to_error_obj,
        filter(lambda ex: ex["loc"][0] == "header", err.errors())
    )
    fields = map(
        map_to_error_obj,
        filter(lambda ex: ex["loc"][0] != "header", err.errors())
    )
    return build_response("Invalid Request", "Missing Required Request Items", status_code=422, headers=dict(headers), fields=dict(fields))