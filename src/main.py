from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from DB.database import Base, engine
from userManagement.routers import router as userManagement_router
from frontend.routers import router as frontend_router
from auth.routers import router as auth_router
from bidManagement.routers import router as bidManagement_router
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv


# Load the environment variables
load_dotenv()

# Create the FastAPI app instance 
app = FastAPI()

# Create the static files route for the frontend
app.mount("/static/", StaticFiles(directory="frontend/static/"), name="static")

# Create the Jinja2 templates instance for the frontend 
templates = Jinja2Templates(directory="frontend/templates")

#routes for authentication module and userManagement module are included 
app.include_router(userManagement_router)
app.include_router(frontend_router)
app.include_router(auth_router)
app.include_router(bidManagement_router)

# Initialize the database
Base.metadata.create_all(bind=engine)
    