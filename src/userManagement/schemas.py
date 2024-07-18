from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
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
    disabled: bool = False
    class Config:
        from_attributes = True