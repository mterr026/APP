#SQLAlchemy models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from DB.database import Base

class User(Base):
    __tablename__ = "user"

    EIN = Column(Integer, primary_key=True, nullable=False, unique=True)
    fName = Column(String, nullable=False)
    lName = Column(String, nullable=False)
    startDate = Column(String, nullable=False)
    role = Column(String, nullable=False)
    securityQuestion = Column(String, nullable=True)
    securityAnswer = Column(String, nullable=True)
    password = Column(String, nullable=False)
    firstLogin = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

class Bids(Base):
    __tablename__ = "bids"
    bidNum = Column(Integer, primary_key=True, nullable=False, unique=True)
    status = Column(String, nullable=False)
    postDate = Column(String, nullable=False)
    closeDate = Column(String, nullable=False)
    description = Column(String, nullable=False)
    hours = Column(Integer, nullable=False)
    awarded = Column(String, default=False)
    daysOff = Column(String, nullable=False)

class bidSelections(Base):
    __tablename__ = "bidSelections"
    id = Column(Integer, nullable=False, unique=True, index=True)
    EIN = Column(Integer, ForeignKey("user.EIN"), primary_key=True, nullable=False)
    bidNum = Column(Integer, ForeignKey("bids.bidNum"), primary_key=True, nullable=False)

    __table_args__ = (
    PrimaryKeyConstraint('EIN', 'bidNum'),
    )

user = relationship("User", back_populates="bids")
bids = relationship("BidSelections", back_populates="user")
selections = relationship("BidSelections", back_populates="bids")


