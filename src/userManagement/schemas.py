from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    EIN: int
    fName: str
    lName: str
    startDate: str
    role: str
    securityQuestion: Optional[str] = None
    securityAnswer: Optional[str] = None
    password: Optional[str] = None
    firstLogin: Optional[str] = "yes"
    currentBid: Optional[str] = "No Bid"

    class Config:
        orm_mode = True
        from_attributes = True