#Where all the activity takes place and where the FastAPI Lives  
from fastapi import FastAPI, HTTPException, Depends
from database import engine, get_db, Base 
from routers.books import router

app = FastAPI(
    title = "Book API", 
    description = "An API that will manage books. POST, PUT, and DELETE require an X-API-Key Header",
    version = "1.0.0"
)

app.include_router(router)        #Connect the routers

@app.get("/")                                               #Root URL 
def read_root():                                            #Run the function
    return {"message": "Hello World"}                       #Return simple, JSON response to prove server is running 