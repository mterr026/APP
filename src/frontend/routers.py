# This file contains the routers for the frontend of the application.
from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from DB import CRUD
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

"""All the routes except the login page are protected by the oauth2Scheme, which is implentented as a dependency from the dependencies.py file."""

######################### USER MANAGEMENT FRONTEND ############################################

# Endpoint to create a new user
@router.get("/createUser")
def createUser(request: Request, message: str = None, currentUser: str = Depends(getCurrentActiveUser)):
    return templates.TemplateResponse("createUser.html", {"request": request, "message": message})

# Endpoint to update a user
@router.get("/updateUser")
def updateUser(request: Request, message: str = None, EIN: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    users = CRUD.CRUD.getUser(db, EIN)
    return templates.TemplateResponse("updateUser.html", {"request": request, "message": message, "users": users})

# Endpoint to view all users
@router.get("/userManagement", response_class=HTMLResponse, response_model=List[schemas.User])
def getUsers(request: Request, 
             db: Session = Depends(get_db),
             currentUser: str = Depends(getCurrentActiveUser)):
    currentUser = currentUser 
    users = CRUD.CRUD.getUsers(db)
    bids = CRUD.CRUD.getBids(db)
    # Create a map of user EIN to bid number to display the name of the employee that has been awarded the bid    
    userBidMap = {user.EIN: None for user in users}
    for bid in bids:
    # Ensure bid.awarded is not None
        if bid.awarded:
            awardedName = bid.awarded.split()
            # Check if the awarded name has exactly two parts (first name and last name)
            if len(awardedName) == 2:
                awardedFirstName, awardedLastName = awardedName
                # Find the user with the matching first and last name
                for user in users:
                    if awardedFirstName == user.fName and awardedLastName == user.lName:
                        # Map the user's EIN to the bid number
                        userBidMap[user.EIN] = bid.bidNum
                        break
    return templates.TemplateResponse("userManagement.html", {"request": request, "users": users, "userBidMap": userBidMap})
#login route or root route
@router.get("/")
def sortByID(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Endpoint to view the first login page 
@router.get("/firstLogin")
def createUser(request: Request, currentUser: User = Depends(getCurrentUser)):
    EIN = currentUser.EIN
    # Check if the user has already logged in before if not stay on the first login page and if yes redirect to the appropriate page
    if currentUser.firstLogin == "no":
        if currentUser.role == "manager":
            return RedirectResponse(url="/awardBid")
        elif currentUser.role == "employee":
            return RedirectResponse(url="/employeeBidView")
        elif currentUser.role == "steward":
            return RedirectResponse(url="/employeeBidView")
    else:
        return templates.TemplateResponse("firstLogin.html", {"request": request, "EIN": EIN, "currentUser": currentUser})

################################## BID MANAGEMENT FRONTEND ############################################    

# Endpoint to create a new bid
@router.get("/bidManagement")
def bidManagement(request: Request, db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBids(db)
    return templates.TemplateResponse("bidManagement.html", {"request": request, "bids": bids})

# Endpoint to create a new bid
@router.get("/createBid")
def createBid(request: Request, currentUser: str = Depends(getCurrentActiveUser)):
    return templates.TemplateResponse("createBid.html", {"request": request})

# Endpoint to edit a bid
@router.get("/editBid")
def updateBid(request: Request, bidNum: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBid(db, bidNum)
    return templates.TemplateResponse("editBid.html", {"request": request, "bids": bids})

# Endpoint to view more in depth details of a bid
@router.get("/bidDetails")
def bidDetails(request: Request, bidNum: int = Query(None), db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBid(db, bidNum)
    currentUser = currentUser
    if bids is None:
        return RedirectResponse(url="/bidManagement?message=Bid not found", status_code=303)
    return templates.TemplateResponse("bidDetails.html", {"request": request, "bids": bids, "current_date": datetime.now().strftime("%Y-%m-%d"), "currentUser": currentUser})

# Endpoint to view all bids
@router.get("/employeeBidView")
def employeeBidView(request: Request, db: Session = Depends(get_db), currentUser: str = Depends(getCurrentActiveUser)):
    bids = CRUD.CRUD.getBids(db)
    employeesSelections = CRUD.CRUD.getEmployeeBids(db, currentUser.EIN)
    return templates.TemplateResponse("employeeView.html", {"request": request, "bids": bids, "employeeBids": employeesSelections, "currentUser": currentUser})

