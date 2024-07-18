from pydantic import BaseModel
from typing import Optional

class BidCreate(BaseModel):
    bidNum: int
    status: str
    postDate: str
    closeDate: str
    description: str
    hours: int
    awarded: bool
    daysOff: int

class BidUpdate(BaseModel):
    bidNum: int
    status: str
    postDate: str
    closeDate: str
    description: str
    hours: int
    awarded: bool
    daysOff: int