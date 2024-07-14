#SQLAlchemy models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from DB.database import Base

class Employee(Base):
    __tablename__ = "employee"

    EIN = Column(Integer, primary_key=True, nullable=False, unique=True)
    fName = Column(String, nullable=False)
    lName = Column(String, nullable=False)
    startDate = Column(String, nullable=False)
    role = Column(String, nullable=False)
    securityQuestion = Column(String, nullable=False)
    securityAnswer = Column(String, nullable=False)
    password = Column(String, nullable=False)
    firstLogin = Column(String, nullable=False)

