# This file contains the CRUD operations for the database
from sqlalchemy.orm import Session
import DB.models
import userManagement
from userManagement import schemas
from dependencies import get_db
import DB

#This class contains the CRUD operations for the database
class CRUD:
    #This function creates a new user in the database
    def creatUser(db: Session, newEmp: DB.models.Employee):
    #Tries to add the new employee to the database
        db.add(newEmp)
        db.commit()
        db.refresh(newEmp)
        #If successful, return success message
        return "REGISTRATION SUCCESSFUL"
    
def updateUser(db: Session, EIN: int, updateUser: DB.models.Employee):
            # Retrieve the employee to update
            employee = db.query(DB.models.Employee).filter(DB.models.Employee.EIN == EIN).first()
            if not employee:
                return "EMPLOYEE NOT FOUND"

            # List of attributes to update
            attributes_to_update = [
                'fName', 'lName', 'startDate', 'role',
                'securityQuestion', 'securityAnswer',
                'password', 'firstLogin'
            ]

            # Update the employee fields with the new data
            for attr in attributes_to_update:
                new_value = getattr(updateUser, attr, None)
                if new_value is not None:
                    setattr(employee, attr, new_value)

            db.commit()
            return "UPDATE SUCCESSFUL"

def removeUser(db: Session, EIN: int):
    # Retrieve the employee to remove
    employee = db.query(DB.models.Employee).filter(DB.models.Employee.EIN == EIN).first()
    if not employee:
        return "EMPLOYEE NOT FOUND"
    else:
    # Remove the employee from the database
        db.delete(employee)
        db.commit()
        return "REMOVAL SUCCESSFUL"

def getUsers(db: Session):
    # Retrieve all employees from the database
    employees = db.query(DB.models.Employee).all()
    return [schemas.Employee.from_orm(employee) for employee in employees]

def getUser(db: Session, EIN: int):
    # Retrieve the employee with the specified EIN
    employee = db.query(DB.models.Employee).filter(DB.models.Employee.EIN == EIN).first()
    if not employee:
        return None
    return schemas.Employee.from_orm(employee)

def userSortByName(db: Session):
    employee = db.query(DB.models.Employee).order_by(DB.models.Employee.fName).all()  
    if not employee:
        return []
    return [schemas.Employee.from_orm(employee) for employees in employee]

      