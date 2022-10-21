import json

from . import build_exc_response

from fastapi import status
from fastapi.responses import JSONResponse

async def handler(_, ex: json.JSONDecodeError):
    return build_exc_response("JSON Decode Error", ex)