# This file contains the dependencies that are used in the FastAPI application
from DB.database import SessionLocal
from fastapi import Depends, HTTPException, status, Request
from auth.businessLogic import oauth2Scheme, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from DB import CRUD
from auth.schemas import UserLogin
from typing import Annotated    
from fastapi.responses import RedirectResponse

# Dependency to get the database session 
def get_db():
    # Create a new session for each request 
    db = SessionLocal()
    # Yield the session to the route 
    try:
        yield db
    finally:
        # Close the session after the request is complete 
        db.close()

# Get the current user for authorization purposes 
def getCurrentUser(request: Request, db: Session = Depends(get_db)):
    # Get the token from the request
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    # Check if the token is a Bearer token and remove it 
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode the token and get the payload 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Get the user from the database using the username from the token payload 
    user = CRUD.CRUD.getUser(db, username)
    if user is None:
        raise credentials_exception
    return user

# Dependency to get the current user and check if they are active or not 
def getCurrentActiveUser(
    currentUser: Annotated[UserLogin, Depends(getCurrentUser)],
):
    if currentUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currentUser