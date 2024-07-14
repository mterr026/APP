# Description: Auth routers for handling user authentication.
from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from classes import Auth
import DB.models
from sqlalchemy.orm import Session
from DB import CRUD
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#This is the router for the userManagement module
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
def protectedRoute(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}

@router.get('/testing')
def test(token: Annotated[str, Depends(oauth2_scheme)]):
    return None

