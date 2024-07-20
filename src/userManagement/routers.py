#all the imported modules are used to create the routes for the userManagement module
from typing import List
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from classes import Manager
from userManagement.businessLogic import password_hash
from sqlalchemy.orm import Session
from DB import CRUD
from dependencies import get_db, getCurrentUser
from DB.models import User

#sets an instance of the APIRouter class to the variable router
router = APIRouter()

# endpoint to create a new user
@router.post("/addUser")
def newUser(
    #Parameters taken from form data
    EIN: int = Form(...),
    fName: str = Form(...),
    lName: str = Form(...),
    startDate: str = Form(...),
    role: str = Form(...),
    password: str = Form(...),
    firstLogin: str = Form("yes"),
    db: Session = Depends(get_db)
): #takes in form data and creates a new user object
    newEmp = User(
        EIN = EIN, 
        fName = fName, 
        lName = lName,
        startDate = startDate, 
        role = role,
        password = password_hash(password),
        firstLogin = firstLogin
        )
    
    #uses the Manager class to create a new user
    try:
        message = Manager.addUser(db, newEmp)
        if message is None:
            message = "Registration failed: Unknown error."
                #If registration is unsuccessful, redirect to create new user page with error message or success message
    except:
        message = f"EIN already exists. Please try again."
    return RedirectResponse(url=f"/createUser?message={message}", status_code=303)

# endpoint to update a user
@router.post("/editUser")
def editUser(
    EIN: int = Form(...),
    startDate: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
):
    update = User(
        startDate = startDate, 
        role = role,
        )
    # Update the user in the database
    message = CRUD.CRUD.updateUser(db, EIN, update)
    if message is None:
        message = "Update failed: Unknown error."
    else:
        message = "Update successful."
    return RedirectResponse(url=f"/updateUser?message={message}", status_code=303)

@router.post("/deleteUser")

#endpoint to delete a user
def deleteUser(EIN: List[int] = Form(...),db: Session = Depends(get_db)):
    # Delete the user from the database
    deleteMessage = ""
    for ein in EIN:
        message = CRUD.CRUD.removeUser(db, ein)
        if message is None:
            deleteMessage += f"Failed to delete EIN {ein}. "
        else:
            deleteMessage += f"Successfully deleted EIN {ein}. "  
    return RedirectResponse(url=f"/userManagement?deleteMessage={deleteMessage}", status_code=303)

#Endpoint to get all users
@router.post("/getUsers")
#This route is used to get all users
def getUsers(db: Session = Depends(get_db)):
    user = CRUD.CRUD.getUsers(db)
    if user is None:
        user = "No users found."
    return RedirectResponse(url=f"/userManagement?user={user}", status_code=303)

#Endpoint to set first time login credentials
@router.post("/register")
def register(
    newPassword: str = Form(...), 
    securityQuestion: str = Form(...), 
    securityAnswer: str = Form(...),
    db: Session = Depends(get_db), 
    user: User = Depends(getCurrentUser)):
    password = password_hash(newPassword)
    securityQuestion = securityQuestion
    securityAnswer = securityAnswer
    EIN = user.EIN
    CRUD.CRUD.registerUser(db, EIN, password, securityQuestion, securityAnswer)
    return RedirectResponse(url="/firstLogin", status_code=303)

