from pydantic import BaseModel

#Pydantic schemas 
#Schema for the User
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
#Schema for the User Login
class UserLogin(BaseModel):
    EIN: str
    role: str
    firstLogin: str
    disabled: bool
    
#Schema for the User in the database
class UserInDB(UserLogin):
    hashed_password: str

