# This file contains all the classes that will be used in the system
import datetime

#this class handles all the authentication for access to the website
class Auth:
    def register():
        pass
    def login():
        pass

#the user class is used as a parent to manager, employee and shopsteward it defines the 
# basic functionality and attributes of each user instance
class User:

    def __init__(self,EIN: int,fName: str,Lname: str,role: str,firstLogin: str,startDate: datetime,password: str,securityQuestion: str,securityAnswer: str):
        self.EIN = EIN
        self.fName = fName
        self.lName = Lname
        self.role = role
        self.firstLogin = firstLogin
        self.startDate = startDate
        self.password = password
        self.securityQuestion = securityQuestion
        self.securityAnswer = securityAnswer
    
    def resetPwd(self):
        pass
    
    def viewBidS(self):
        pass
    
    def sortBid(self):
        pass
    
class Employee(User):

    def selectBid(self):
        pass
    

#shop steward  sub class of User   
class ShopSteward(User):
    pass

#This is the class that will handle all user mangement, for creating, editing, removing or adding new employees
class Manager(User):

######################################## User Management ############################################
    def sortBids(self):
        pass
    
    def resetPwd(self):
        pass

    def createUser(self):
        pass

    def editUser(self):
        pass

    def removeUser(self):
        pass

    def addUser(self):
        pass

    def getUsers(self):
        pass
    
    ############################### Bid management section ################################

    def createBid(self):
        pass

    def editBid(self):
        pass

    def removeBid(self):
        pass

    def addBid(self):
        pass
    
class Bids:
    def __init__(self,bidNum: int,status: str,postDate: datetime,closeDate: datetime,description: str,hours: int,awarded: str,daysOff: str):
        self.bidNum = bidNum
        self.status = status
        self.postDate = postDate
        self.closeDate = closeDate
        self.description = description
        self.hours = hours
        self.awarded = awarded
        self.daysOff = daysOff
      
    def awardBid(self):
        pass