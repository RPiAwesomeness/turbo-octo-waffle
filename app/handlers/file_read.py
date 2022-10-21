from http import client

from . import build_exc_response

from fastapi import Request, status
from fastapi.responses import JSONResponse

async def handler(request: Request, ex: client.IncompleteRead):
    return build_exc_response("Read Error", ex, filename=await request.form()['file'].filename)