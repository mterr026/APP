#all the imported modules are used to create the routes for the userManagement module
from typing import List
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from classes import Manager
from userManagement.businessLogic import password_hash
import DB
import DB.models
from sqlalchemy.orm import Session
from DB import CRUD

#This is the router for the userManagement module
router = APIRouter()

#This route is used to create a new user
@router.post("/addUser")
def newUser(
    #Parameters taken from form data
    EIN: int = Form(...),
    fName: str = Form(...),
    lName: str = Form(...),
    startDate: str = Form(...),
    role: str = Form(...),
    securityQuestion: str = Form(...),
    securityAnswer: str = Form(...),
    password: str = Form(...),
    firstLogin: str = Form("yes"),
    db: Session = Depends(get_db)
): #takes in form data and creates a new employee object
    newEmp = DB.models.Employee(
        EIN = EIN, 
        fName = fName, 
        lName = lName,
        startDate = startDate, 
        role = role,
        securityQuestion = securityQuestion, 
        securityAnswer = securityAnswer, 
        password = password_hash(password),
        firstLogin = firstLogin
        )
    #uses the Manager class to create a new user
    message = Manager.addUser(db, newEmp)
    if message is None:
        message = "Registration failed: Unknown error."
            #If registration is unsuccessful, redirect to create new user page with error message or success message
    return RedirectResponse(url=f"/createUser?message={message}", status_code=303)

@router.post("/editUser")
#This route is used to update an existing user
def editUser(
    EIN: int = Form(...),
    fName: str = Form(...),
    lName: str = Form(...),
    startDate: str = Form(...),
    role: str = Form(...),
    securityQuestion: str = Form(...),
    securityAnswer: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    update = DB.models.Employee(
        EIN = EIN, 
        fName = fName, 
        lName = lName,
        startDate = startDate, 
        role = role,
        securityQuestion = securityQuestion, 
        securityAnswer = securityAnswer, 
        password = password_hash(password),
        )
    # Update the user in the database
    message = CRUD.updateUser(db, EIN, update)
    if message is None:
        message = "Update failed: Unknown error."
    else:
        message = "Update successful."
    return RedirectResponse(url=f"/updateUser?message={message}", status_code=303)

@router.post("/deleteUser")
#This route is used to delete a user
def deleteUser(EIN: List[int] = Form(...),db: Session = Depends(get_db)):
    # Delete the user from the database
    deleteMessage = ""
    for ein in EIN:
        message = CRUD.removeUser(db, ein)
        if message is None:
            deleteMessage += f"Failed to delete EIN {ein}. "
        else:
            deleteMessage += f"Successfully deleted EIN {ein}. "  
    return RedirectResponse(url=f"/userManagement?deleteMessage={deleteMessage}", status_code=303)

@router.post("/getUsers")
#This route is used to get all users
def getUsers(db: Session = Depends(get_db)):
    employee = CRUD.getUsers(db)
    if employee is None:
        employee = "No users found."
    return RedirectResponse(url=f"/userManagement?employee={employee}", status_code=303)

