import DB
from fastapi import Depends
from datetime import datetime
from DB import schemas as DB
import DB.models
from DB import CRUD
from sqlalchemy.orm import Session
import classes
from dependencies import get_db

def createBid(db: Session, newBid: DB.models.Bids):
    message = CRUD.CRUD.createBid(db, newBid)
    return message

def updateBid(db: Session, bidNum: int, updateBid: DB.models.Bids):
    message = CRUD.CRUD.updateBid(db, bidNum, updateBid)
    return message

def removeBid(db: Session, bidNum: int):
    message = CRUD.CRUD.removeBid(db, bidNum)
    return message

def getBids(db: Session):
    bids = CRUD.CRUD.getBids(db)
    return bids

def getBid(db: Session, bidNum: int):
    bid = CRUD.CRUD.getBid(db, bidNum)
    return bid

def checkExistingBid(db: Session, bidNum: int, EIN: int):
    return db.query(DB.models.Bids).filter(DB.models.bidSelections.bidNum == bidNum, DB.models.bidSelections.EIN == EIN).first()

def placeBid(db: Session, bidNum: int, EIN: int):
    bid = CRUD.CRUD.placeBid(db, bidNum, EIN ) 

classes.Manager.createBid = createBid
classes.Manager.editBid = updateBid
classes.Manager.removeBid = removeBid   
classes.User.viewBidS = getBids

