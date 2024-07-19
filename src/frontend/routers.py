# This file contains the routers for the frontend of the application.
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Query, Request, Depends, Form, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from DB import CRUD, models
from sqlalchemy.orm import Session
from dependencies import get_db, getCurrentUser, getCurrentActiveUser
from auth.businessLogic import oauth2Scheme
from DB.models import User  
from datetime import datetime
from typing import List
from DB import schemas
router = APIRouter()

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="frontend/templates")

######################### USER MANAGEMENT FRONTEND ############################################
@router.get("/createUser")
def createUser(request: Request, message: str = None, currentUser: str = Depends(getCurrentActiveUser)):
    return templates.TemplateResponse("createUser.html", {"request": request, "message": message})

@router.get("/updateUser")
def updateUser(request: Request, message: str = None, EIN: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    users = CRUD.CRUD.getUser(db, EIN)
    return templates.TemplateResponse("updateUser.html", {"request": request, "message": message, "users": users})

@router.get("/userManagement", response_class=HTMLResponse, response_model=List[schemas.User])
def getUsers(request: Request, 
             db: Session = Depends(get_db),
             currentUser: str = Depends(getCurrentActiveUser)): 
    users = CRUD.CRUD.getUsers(db)
    return templates.TemplateResponse("userManagement.html", {"request": request, "users": users})

@router.get("/")
def sortByID(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/firstLogin")
def createUser(request: Request, currentUser: User = Depends(getCurrentUser)):
    EIN = currentUser.EIN
    if currentUser.firstLogin == "no":
        if currentUser.role == "manager":
            return RedirectResponse(url="/userManagement")
        elif currentUser.role == "employee":
            return RedirectResponse(url="/employeeBidView")
        elif currentUser.role == "steward":
            return RedirectResponse(url="/employeeBidView")
    else:
        return templates.TemplateResponse("firstLogin.html", {"request": request, "EIN": EIN})
    
@router.get("/bidManagement")
def bidManagement(request: Request, db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBids(db)
    return templates.TemplateResponse("bidManagement.html", {"request": request, "bids": bids})

@router.get("/createBid")
def createBid(request: Request, currentUser: str = Depends(getCurrentActiveUser)):
    return templates.TemplateResponse("createBid.html", {"request": request})

@router.get("/editBid")
def updateBid(request: Request, bidNum: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBid(db, bidNum)
    return templates.TemplateResponse("editBid.html", {"request": request, "bids": bids})

@router.get("/bidDetails")
def bidDetails(request: Request, bidNum: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBid(db, bidNum)
    currentUser = currentUser
    if bids is None:
        return RedirectResponse(url="/bidManagement?message=Bid not found", status_code=303)
    return templates.TemplateResponse("bidDetails.html", {"request": request, "bids": bids, "current_date": datetime.now().strftime("%Y-%m-%d"), "currentUser": currentUser})

@router.get("/employeeBidView")
def employeeBidView(request: Request, db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBids(db)
    employeesSelections = CRUD.CRUD.getEmployeeBids(db, currentUser.EIN)
    return templates.TemplateResponse("employeeView.html", {"request": request, "bids": bids, "employeeBids": employeesSelections})