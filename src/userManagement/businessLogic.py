# This file contains the business logic for the user management module. It contains the functions for registering and logging in users.
import DB
import bcrypt
import DB.models
from sqlalchemy.orm import Session
from DB import CRUD
import classes

#Hashes password with bcrypt algorithm
def password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  

# function to add a user to the database using the crud operation from the DB
def addUser(db, newEmp):
    message = CRUD.CRUD.creatUser(db, newEmp)
    return message

# function to update a user in the database
def updateUser(db, EIN: int, update: DB.models.User):
    message = CRUD.CRUD.updateUser(db, EIN, update)
    if message is None:
        message = "Update failed: Unknown error."

# function to remove a user from the database
def removeUser(db, EIN):
    message = CRUD.CRUD.removeUser(db, EIN)
    if message is None:
        message = "Removal failed: Unknown error."

# function to get all users from the database
def getUsers(db):
    employee = CRUD.CRUD.getUsers(db)
    return employee

# function to get all users with bids from the database
def getUsersWithBids(db: Session):
    users = db.query(DB.models.User).all()
    for user in users:
        current_bid = db.query(DB.models.Bids).filter(DB.models.Bids.awarded == f"{user.fName} {user.lName}").first()
        if current_bid:
            user.currentBid = f"Bid Number: {current_bid.bidNum}, Status: {current_bid.status}"
        else:
            user.currentBid = "No current bid"
    return users
    
classes.Manager.removeUser = removeUser
classes.Manager.addUser = addUser
classes.Manager.editUser = updateUser
classes.Manager.getUsers = getUsers



