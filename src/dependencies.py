# This file contains the dependencies that are used in the FastAPI application
from DB.database import SessionLocal
from fastapi import Form
from auth.schemas import EmployeeCreate

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

