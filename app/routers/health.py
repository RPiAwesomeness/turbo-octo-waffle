from datetime import datetime
from enum import Enum, unique
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, conint

router = APIRouter(prefix="/health")

@unique
class StatusString(Enum):
    UP = "up"
    DOWN = "down"

class ServiceStatus(BaseModel):
    id: str
    name: str
    timestamp: datetime
    tags: list[str] = []
    status: StatusString = "down"
    message: str | None = None
    connectionId: str | None = None

class ListResponse(BaseModel):
    services: list[ServiceStatus] = []

class CountResponse(BaseModel):
    up: int
    down: int
    total: int

@router.get("/list", response_model=ListResponse, response_model_exclude_unset=True)
def status_list(query: str | None = None, status: StatusString | None = None, tags: list[str] | None = Query(default=None)):
    return {
        "THIS-FIELD-WILL-BE-IGNORED": {},
        "services": [
            {
                "id": query if query is not None else "foo",
                "THIS-FIELD-WILL-BE-STRIPPED": 42,
                "name": "bar",
                "timestamp": datetime.utcnow(),
                "tags": tags if isinstance(tags, list) else [],
                "status": status if isinstance(status, ServiceStatus) else StatusString.UP
            }
        ]
    }

@router.get("/tags", response_model=list[str])
def get_tags():
    return [
        "zeus",
        "hera",
        "hades",
        "persephone",
    ]

@router.get("/count", response_model=CountResponse)
def get_count():
    return {
        "up": 0,
        "down": 0,
        "total": 0
    }