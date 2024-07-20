#Pydantic schemas
from pydantic import BaseModel
from typing import Optional
class User(BaseModel):
    EIN: str
    fName: str
    lName: str
    startDate: str
    role: str
    securityQuestion: str
    securityAnswer: str
    password: str
    disabled: bool  # Ensure this attribute is included

    class Config:
        orm_mode = True

class Bids(BaseModel):
    bidNum: int
    status: str
    postDate: str
    closeDate: str
    description: str
    hours: int
    awarded: Optional[str] = None
    daysOff: str

    class Config:
        orm_mode = True

class BidsCreate(Bids):
    pass

class Bids(Bids):
    class Config:
        from_attributes = True

class Postings(BaseModel):
    postID: int
    EIN: int
    bidNum: int
    awardTo: int
    requestDate: str
    awardDate: str

    class Config:
        orm_mode = True