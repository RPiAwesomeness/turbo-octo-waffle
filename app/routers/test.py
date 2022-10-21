import http
import json
from fastapi import APIRouter, Depends, File, HTTPException, Header, UploadFile

router = APIRouter(prefix="/test")

async def verify_fake_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header mismatch")

async def verify_lemons(x_lemons: str = Header()):
    if x_lemons == "make-lemonade" or x_lemons != "get-mad":
        raise HTTPException(status_code=400, detail="X-Lemons header mismatch")

# NOTE: File handling requires python-multipart (pip install python-multipart)
@router.post("/files")
def files(file: bytes = File()):
    return {
        "len": len(file)
    }

@router.post("/upload")
async def upload_file(file: UploadFile):
    return {
        "filename": file.filename,
        "headers": file.headers,
        "contents": json.loads(await file.read())
    }

@router.get("/cake", dependencies=[Depends(verify_fake_token), Depends(verify_lemons)])
def secured():
    return {
        "secret": "The cake is a lie"
    }