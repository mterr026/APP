from pydantic import BaseModel, Field
from fastapi import Form, Query
import classes
class EmployeeCreate(BaseModel):
    EIN: int
    fName: str 
    lName: str
    startDate: str
    role: str
    securityQuestion: str 
    securityAnswer: str 
    password: str 
    firstLogin: str 


