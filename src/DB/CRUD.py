# This file contains the CRUD operations for the database
from sqlalchemy.orm import Session
import DB.models
from userManagement import schemas
from DB.schemas import User as UserSchema, Bids as BidsSchema, Postings as PostingsSchema


############################### USER MANAGEMENT CRUD OPERATIONS ############################################

#This class contains the CRUD operations for the database
class CRUD:
    # Creates a new user in the database
    def creatUser(db: Session, newUser: DB.models.User):
    # Tries to add the new users to the database
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        #If successful, return success message
        return "USER CREATION SUCCESSFUL"
    
    def updateUser(db: Session, EIN: int, updateUser: DB.models.User):
            # Retrieve the users to update
            user = db.query(DB.models.User).filter(DB.models.User.EIN == EIN).first()
            if not user:
                return "USER NOT FOUND"

            # List of attributes to update
            attributes_to_update = [
                'startDate', 'role'
            ]

            # Update the users fields with the new data
            for attr in attributes_to_update:
                new_value = getattr(updateUser, attr, None)
                if new_value is not None:
                    setattr(user, attr, new_value)

            db.commit()
            return "UPDATE SUCCESSFUL"

    def removeUser(db: Session, EIN: int):
        # Retrieve the user to remove
        user = db.query(DB.models.User).filter(DB.models.User.EIN == EIN).first()
        if not user:
            return "USER NOT FOUND"
        else:
        # Remove the users from the database
            db.delete(user)
            db.commit()
            return "REMOVAL SUCCESSFUL"
    # Retrieves all users from the database
    def getUsers(db: Session):
        # Retrieve all users from the database
        users = db.query(DB.models.User).all()
        return [schemas.User.from_orm(user) for user in users]

    # Retrieves a user from the database
    def getUser(db: Session, EIN: int):
        # Retrieve the user with the specified EIN
        user = db.query(DB.models.User).filter(DB.models.User.EIN == EIN).first()
        if not user:
            return None
        return schemas.User.from_orm(user)
    # Retrieves a user from the database
    def getUserById(db: Session, EIN: int):
            return db.query(DB.models.User).filter(DB.models.User.EIN == EIN).first()

    # Sets new credentials during first login for a user
    def registerUser(db: Session, EIN: int, Password: str, SecurityQuestion: str, SecurityAnswer: str):
        # Retrieve the user with the specified EIN
        user = db.query(DB.models.User).filter(DB.models.User.EIN == EIN).first()
        if not user:
            return None
        user.securityQuestion = SecurityQuestion
        user.securityAnswer = SecurityAnswer
        user.password = Password
        user.firstLogin = "no"
        db.commit()
        print(user.EIN)
        return "REGISTRATION SUCCESSFUL"

    ############################### BID MANAGEMENT CRUD OPERATIONS ############################################

    def createBid(db: Session, newBid: DB.models.Bids):
        #Tries to add the new bid to the database
        db.add(newBid)
        db.commit()
        db.refresh(newBid)
        #If successful, return success message
        return "BID CREATIONS SUCCESSFUL"     

    def updateBid(db: Session, bidNum: int, updateBid: DB.models.Bids):
        # Retrieve the bid to update
        bid = db.query(DB.models.Bids).filter(DB.models.Bids.bidNum == bidNum).first()
        if not bid:
            return "BID NOT FOUND"

        # List of attributes to update
        attributes_to_update = [
            'status', 'postDate', 'closeDate', 'description', 'hours', 'awarded', 'daysOff'
        ]

        # Update the bid fields with the new data
        for attr in attributes_to_update:
            new_value = getattr(updateBid, attr, None)
            if new_value is not None:
                setattr(bid, attr, new_value)

        db.commit()
        return "UPDATE SUCCESSFUL"

    def removeBid(db: Session, bidNum: int):
        # Retrieve the bid to remove
        bid = db.query(DB.models.Bids).filter(DB.models.Bids.bidNum == bidNum).first()
        if not bid:
            return "BID NOT FOUND"
        else:
        # Remove the bid from the database
            db.delete(bid)
            db.commit()
            return "REMOVAL SUCCESSFUL"
    # Retrieves all bids from the database
    def getBids(db: Session):
        bids = db.query(DB.models.Bids).all()
        return [BidsSchema.from_orm(bid) for bid in bids]
    # Retrieves a bid from the database
    def getBid(db: Session, bidNum: int):
        # Retrieve the bid with the specified bid number
        bid = db.query(DB.models.Bids).filter(DB.models.Bids.bidNum == bidNum).first()
        if not bid:
            return None
        return BidsSchema.from_orm(bid)
    # Retrieves a bid from the database based on the bid number
    def getBidById(db: Session, bidNum: int):
        return db.query(DB.models.Bids).filter(DB.models.Bids.bidNum == bidNum).first()
        
    #add employee bid selection
    def placeBid(db: Session, bidNum: int, EIN: int):
        # Create a new bid selection
        newBidSelection = DB.models.bidSelections(
            EIN = EIN,
            bidNum = bidNum
        )
        # Add the new bid selection to the database
        db.add(newBidSelection)
        db.commit()
        db.refresh(newBidSelection)
        return "BID PLACEMENT SUCCESSFUL"
    
    # Used to retireve bids that the employee has selected and is awaiting awarding 
    def getEmployeeBids(db: Session, EIN: int):
         return db.query(DB.models.Bids).join(DB.models.bidSelections).filter(DB.models.bidSelections.EIN == EIN).all()
    
    # Cancels the bid request and removes it from the table bidSelections
    def cancelBidRequest(db: Session, bidNum: int, EIN: int):
        db.query(DB.models.bidSelections).filter(DB.models.bidSelections.bidNum == bidNum, DB.models.bidSelections.EIN == EIN).delete()
        db.commit()
        return "BID CANCELLED"