from fastapi.security import OAuth2PasswordBearer
from DB import CRUD
from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Securely load environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "backupSecretKey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the OAuth2 scheme for password bearer token
oauth2Scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "manager": "Access manager functionalities",
        "employee": "Access employee functionalities",
        "shop_steward": "Access shop steward functionalities"
    }
)

# Verify the password using bcrypt
def verifyPassword(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Authenticate the user
def authenticateUser(db: Session, username: str, password: str):
    # Get the user from the database
    user = CRUD.CRUD.getUserById(db, username)
    if not user or not verifyPassword(password, user.password):
        return False
    return user

# Create an access token
def createAccessToken(data: dict, expiresDelta: timedelta = None):
    # Copy the data to avoid modifying the original
    toEncode = data.copy()
    # Set the expiration time for the token
    if expiresDelta:
        expire = datetime.now(timezone.utc) + expiresDelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire, "sub": str(data["sub"])})
    # Encode the token using the secret key and algorithm
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt


