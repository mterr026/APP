# This file contains the business logic for the bid management module
import DB
from datetime import datetime
from DB import schemas as DB
import DB.models
from DB import CRUD
from sqlalchemy.orm import Session
import classes

# Function to create a new bid
def createBid(db: Session, newBid: DB.models.Bids):
    message = CRUD.CRUD.createBid(db, newBid)
    return message

# Function to update a bid
def updateBid(db: Session, bidNum: int, updateBid: DB.models.Bids):
    message = CRUD.CRUD.updateBid(db, bidNum, updateBid)
    return message
# Function to remove a bid
def removeBid(db: Session, bidNum: int):
    message = CRUD.CRUD.removeBid(db, bidNum)
    return message
# Function to get all bids
def getBids(db: Session):
    bids = CRUD.CRUD.getBids(db)
    return bids

# Function to get a specific bid
def getBid(db: Session, bidNum: int):
    bid = CRUD.CRUD.getBid(db, bidNum)
    return bid

#checks if a bid exists based on the bid number and EIN to ensure one user can't place multiple requests on one bid
def checkExistingBid(db: Session, bidNum: int, EIN: int):
    return db.query(DB.models.Bids).filter(DB.models.bidSelections.bidNum == bidNum, DB.models.bidSelections.EIN == EIN).first()
# Function to place a bid
def placeBid(db: Session, bidNum: int, EIN: int):
    bid = CRUD.CRUD.placeBid(db, bidNum, EIN ) 

# awards the bid to the employee with the oldest start date
def awardBid(db: Session):
    current_date = datetime.now().strftime("%Y-%m-%d")
    closed_bids = db.query(DB.models.Bids).filter(DB.models.Bids.closeDate < current_date, DB.models.Bids.status != 'awarded').all()

    for bid in closed_bids:
        # Get all selections for the bid
        selections = db.query(DB.models.bidSelections).filter(DB.models.bidSelections.bidNum == bid.bidNum).all()
        if selections:
            # Find the employee with the oldest start date and award the bid to them
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

# Function to cancel a bid request
def cancelBidRequest(db: Session, bidNum: int, EIN: int):
    CRUD.CRUD.cancelBidRequest(db, bidNum, EIN)


classes.Manager.createBid = createBid
classes.Manager.editBid = updateBid
classes.Manager.removeBid = removeBid   
classes.User.viewBidS = getBids
classes.Bids.awardBid = awardBid
classes.Employee.selectBid = placeBid


