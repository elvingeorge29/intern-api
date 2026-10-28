import os                   
from dotenv import load_dotenv

load_dotenv()                                           #Reads all the lines 

DATABASE_URL = os.getenv("DATABASE_URL")                #Checks for URL enviornment variable 
BOOKS_API_KEY = os.getenv("BOOKS_API_KEY")              #Checks for API Key enviornment variable 

if not DATABASE_URL: 
    raise ValueError("ERROR: DATABASE_URL missing from the .env file")  #Crash if the URL is missing 
if not BOOKS_API_KEY:
    raise ValueError("ERROR: BOOKS_API_KEY missing from the .env file ")    #Crash if the API Key is Missing