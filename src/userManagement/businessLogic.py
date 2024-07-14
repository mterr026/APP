# This file contains the business logic for the user management module. It contains the functions for registering and logging in users.
import DB
import bcrypt
import DB.models
from sqlalchemy.orm import Session
from DB import CRUD
import classes
from dependencies import get_db
from fastapi import Depends, Form

#Hashes password with bcrypt algorithm
def password_hash(password: str):
    salt = bcrypt.gensalt(rounds=12)
    bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytes, salt)

    return hashed

#This function adds a user to the database
def addUser(db, newEmp):
    message = CRUD.CRUD.creatUser(db, newEmp)
    return message

#This function updates a user in the database
def updateUser(db, EIN: int, update: DB.models.Employee):
    message = CRUD.updateUser(db, EIN, update)
    if message is None:
        message = "Update failed: Unknown error."

#This function removes a user from the database
def removeUser(db, EIN):
    message = CRUD.removeUser(db, EIN)
    if message is None:
        message = "Removal failed: Unknown error."

#This function retrieves all users from the database
def getUsers(db):
    employee = CRUD.getUsers(db)
    return employee

classes.Manager.removeUser = removeUser
classes.Manager.addUser = addUser
classes.Manager.editUser = updateUser
classes.Manager.getUsers = getUsers
