from typing import List
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from classes import Bids
from DB import models
from bidManagement import businessLogic

#This is the router for the bidManagement module
router = APIRouter()

@router.post("/newBid")
def newBid(
    bidNum: int = Form(...),
    status: str = Form(...),
    postDate: str = Form(...),
    closeDate: str = Form(...),
    description: str = Form(...),
    hours: int = Form(...),
    awarded: bool = Form(...),
    daysOff: str = Form(...),
    db: Session = Depends(get_db),
):
    newBid = models.Bids(
        bidNum = bidNum,
        status = status,
        postDate = postDate,
        closeDate = closeDate,
        description = description,
        hours = hours,
        awarded = awarded,
        daysOff = daysOff
    )
    message = businessLogic.createBid(db, newBid)
    return RedirectResponse(url=f"/bidManagement?message={message}", status_code=303)

@router.post("/updateBid")
def updateBid(
    bidNum: int = Form(...),
    status: str = Form(...),
    postDate: str = Form(...),
    closeDate: str = Form(...),
    description: str = Form(...),
    hours: int = Form(...),
    awarded: str = Form(...),
    daysOff: str = Form(...),
    db: Session = Depends(get_db),
):
    bid = models.Bids(
        bidNum = bidNum,
        status = status,
        postDate = postDate,
        closeDate = closeDate,
        description = description,
        hours = hours,
        awarded = awarded,
        daysOff = daysOff
    )
    message = businessLogic.updateBid(db, bidNum, bid)
    return RedirectResponse(url=f"/bidManagement?message={message}", status_code=303)

@router.post("/deleteBid")
def deleteBid(
    bidNum: int = Form(...),
    db: Session = Depends(get_db),
):
    message = businessLogic.removeBid(db, bidNum)
    return RedirectResponse(url=f"/bidManagement?message={message}", status_code=303)

@router.post("/placeBid")
def placeBid(
    bidNum: int = Form(...),
    EIN: int = Form(...),
    db: Session = Depends(get_db),
):
    # Check if the bid already exists for the given EIN and bidNum
    existingBid = businessLogic.checkExistingBid(db, EIN)
    if existingBid:
        message = "You have already placed a bid on this posting."
    else:
        businessLogic.placeBid(db, bidNum, EIN, postingID)
        message = "You have Placed this bid"
    
    return RedirectResponse(url=f"/bidDetails?bidNum={bidNum}&message={message}", status_code=303)