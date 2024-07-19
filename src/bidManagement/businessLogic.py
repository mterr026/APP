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

def awardBid(db: Session):
    current_date = datetime.now().strftime("%Y-%m-%d")
    closed_bids = db.query(DB.models.Bids).filter(DB.models.Bids.closeDate < current_date, DB.models.Bids.status != 'awarded').all()

    for bid in closed_bids:
        # Get all selections for the bid
        selections = db.query(DB.models.bidSelections).filter(DB.models.bidSelections.bidNum == bid.bidNum).all()
        if selections:
            # Find the employee with the oldest start date who hasn't been awarded a bid yet
            selectedEmployee = None
            oldestStartDate = None
            for selection in selections:
                employee = db.query(DB.models.User).filter(DB.models.User.EIN == selection.EIN).first()
                if employee:
                    if oldestStartDate is None or employee.startDate < oldestStartDate:
                        selectedEmployee = employee
                        oldestStartDate = employee.startDate
            
            if selectedEmployee:
                # Update the status of previously awarded bids for the selected employee
                previously_awarded_bids = db.query(DB.models.Bids).filter(DB.models.Bids.awarded == f"{selectedEmployee.fName} {selectedEmployee.lName}", DB.models.Bids.status == "awarded").all()
                for prev_bid in previously_awarded_bids:
                    prev_bid.awarded = None
                    prev_bid.status = "vacant"

                # Update the awarded field and status in the current bid
                bid.awarded = f"{selectedEmployee.fName} {selectedEmployee.lName}"
                bid.status = "awarded"
                
                # Delete all bid selections for the specific bid
                db.query(DB.models.bidSelections).filter(DB.models.bidSelections.bidNum == bid.bidNum).delete()
                
                db.commit()



classes.Manager.createBid = createBid
classes.Manager.editBid = updateBid
classes.Manager.removeBid = removeBid   
classes.User.viewBidS = getBids

