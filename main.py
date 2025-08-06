##MAIN##

#import files for front-end, backend, dev, ai models

from fastapi import FastAPI
from app.api import fall_event

app = FastAPI()

app.include_router(fall_event.router, prefix="/fall_event", tags=["Fall Events"])

#load files and data using APIs

#define variables with data

#call functions on variables#

#if user data/information records are empty
    #prompt login page/profile page
    #display message prompting them to fill in information

#else if user information is there
    #display home page from front end 
        #load data from backend to front end
        #load core functionality
