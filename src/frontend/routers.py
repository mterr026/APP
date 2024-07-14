from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Query, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from DB import CRUD
from sqlalchemy.orm import Session
from dependencies import get_db
from auth.routers import oauth2_scheme

router = APIRouter()

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="frontend/templates")


######################### USER MANAGEMENT FRONTEND ############################################
@router.get("/createUser")
def createUser(request: Request, message: str = None):
    return templates.TemplateResponse("createUser.html", {"request": request, "message": message})

@router.get("/updateUser")
def updateUser(request: Request, message: str = None, EIN: int = Query(None), db: Session = Depends(get_db)):
    employees = CRUD.getUser(db, EIN)
    return templates.TemplateResponse("updateUser.html", {"request": request, "message": message, "employees": employees})

@router.get("/userManagement", response_class=HTMLResponse)
def getUsers(request: Request, deleteMessage: str = None, db: Session = Depends(get_db)):
    employees = CRUD.getUsers(db)
    return templates.TemplateResponse("userManagement.html", {"request": request, "deleteMessage": deleteMessage, "employees": employees})

@router.get("/userManagement/userSortByName")
def sortByID(request: Request, db: Session = Depends(get_db)):
    employees = CRUD.userSortByName(db)
    return templates.TemplateResponse("userManagement.html", {"request": request, "employees": employees})