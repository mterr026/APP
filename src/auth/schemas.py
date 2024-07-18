from pydantic import BaseModel, Field
from fastapi import Form, Query
import classes

class UserCreate(BaseModel):
    EIN: int
    fName: str 
    lName: str
    startDate: str
    role: str
    securityQuestion: str 
    securityAnswer: str 
    password: str 
    firstLogin: str 

class UserLogin(BaseModel):
    EIN: str
    role: str
    firstLogin: str
    disabled: bool

class UserInDB(UserLogin):
    hashed_password: str

