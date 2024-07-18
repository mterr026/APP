from datetime import timedelta, datetime, timezone
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies import get_db
from auth.businessLogic import ACCESS_TOKEN_EXPIRE_MINUTES, authenticateUser, createAccessToken
from DB.models import User
import os

#This is the router for the auth module
router = APIRouter()

#Endpoint to log in and get an access token
@router.post("/token")
#This function logs in a user and returns an access token to the user 
def loginForAccessToken(response: Response, formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Uses formdata to get the username and password and authenticate the user 
    user = authenticateUser(db, formData.username, formData.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #Creates an access token for the user and sets it as a cookie with expiration time
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(
        data={"sub": user.EIN}, expiresDelta=accessTokenExpires
    )
    secure = os.getenv("SECURE_COOKIES", "False").lower() == "true"
    response.set_cookie(key="accessToken", value=accessToken, httponly=True, secure=secure, samesite='Strict')
    
    return {"accessToken": accessToken, "token_type": "bearer"}

#Endpoint to log out and delete the access token
@router.post("/logout")
def logout(response: Response):
    secure = os.getenv("SECURE_COOKIES", "False").lower() == "true"

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="accessToken", path='/', httponly=True, secure=secure, samesite='Strict')
    response.headers["Cache-Control"] = "no-store"
    return response
