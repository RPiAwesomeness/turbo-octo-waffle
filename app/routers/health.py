from datetime import datetime
from enum import Enum, unique
from optparse import Option
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query
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
    tags: List[str] = []
    status: StatusString = "down"
    message: Optional[str] = None
    connectionId: Optional[str] = None

class ServiceListResponse(BaseModel):
    services: List[ServiceStatus] = []

class CountResponse(BaseModel):
    up: int
    down: int
    total: int

class ServicesWithCount(ServiceListResponse):
    """An example extension class to show how inheritance is handled in a response model context"""
    count: CountResponse

class CommonFilterParams:
    """This class is a simple example of FastAPI's dependency injection for some common parameters"""

    def __init__(self, query: Optional[str] = None, status: Optional[StatusString] = None, tags: Optional[List[str]] = Query(default=None)):
        self.query = query
        self.status = status
        self.tags = tags
        
"""
The response_model argument to the route decorator must be typed with `Union` because it is an argument and not just a type annotation.
This could also be achieved using `response_model_exclude_unset` and an optional `count` field but this serves as an example of what can be done

NOTE: The more specific/inheriting types must be declared first in the Union (eg. ServicesWithCount extends/inherits 
      ServiceListResponse so it goes before ServiceListResponse)

NOTE: The common filter params depedency is called here without an argument to Depends. This is because it picks up the type from the hint O_O
"""
@router.get("/list", response_model=Union[ServicesWithCount, ServiceListResponse], response_model_exclude_unset=True)
def status_list(filters: CommonFilterParams = Depends(), with_count: bool = False):
    resp = {
        "THIS-FIELD-WILL-BE-IGNORED": {},
        "services": [
            {
                "id": filters.query if filters.query is not None else "foo",
                "THIS-FIELD-WILL-BE-STRIPPED": 42,
                "name": "bar",
                "timestamp": datetime.utcnow(),
                "tags": filters.tags if isinstance(filters.tags, list) else [],
                "status": filters.status if isinstance(filters.status, ServiceStatus) else StatusString.UP
            }
        ]
    }

    if with_count:
        print("with_count")
        resp.setdefault(
            "count",
            {
                "up": 1 if resp["services"][0]["status"] == "up" else 0,
                "down": 0 if resp["services"][0]["status"] == "up" else 1,
                "total": 1
            }
        )
    
    return resp

@router.get("/tags", response_model=List[str])
def get_tags():
    return [
        "zeus",
        "hera",
        "hades",
        "persephone",
    ]

@router.get("/count", response_model=CountResponse)
def get_count(_filters: CommonFilterParams = Depends(CommonFilterParams)):
    return {
        "up": 0,
        "down": 0,
        "total": 0
    }