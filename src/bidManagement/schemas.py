from pydantic import BaseModel
from typing import Optional

class BidCreate(BaseModel):
    bidNum: int
    status: str
    postDate: str
    closeDate: str
    description: str
    hours: int
    awarded: str
    daysOff: str

class BidUpdate(BaseModel):
    bidNum: int
    status: str
    postDate: str
    closeDate: str
    description: str
    hours: int
    awarded: str
    daysOff: str