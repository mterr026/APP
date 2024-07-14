# Description: This file is the main entry point for the FastAPI application. It creates the FastAPI app, initializes the database, and includes the routers for the different modules.
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from fastapi.staticfiles import StaticFiles
from DB.database import Base, engine
from userManagement.routers import router as userManagement_router
from frontend.routers import router as frontend_router
from auth.routers import router as auth_router
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dependencies import get_db

# Create the FastAPI app
app = FastAPI()

# Create the static files route
app.mount("/static/", StaticFiles(directory="frontend/static/"), name="static")

# Create the Jinja2 templates
templates = Jinja2Templates(directory="frontend/templates")

#routes for authentication module
app.include_router(userManagement_router)
app.include_router(frontend_router)
app.include_router(auth_router)

# Define the root route
@app.get('/')
def root():
    return None

# Initialize the database
Base.metadata.create_all(bind=engine)

# Test the database connection will be removed in final version
@app.get("/test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Run a simple query to test the connection
        result = db.execute(text("SELECT 1"))
        # Convert the result to a list of dictionaries
        result_list = [{"result": row[0]} for row in result]
        return {"status": "Connection successful", "result": result_list}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}
    