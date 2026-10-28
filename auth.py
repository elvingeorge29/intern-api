from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from config import BOOKS_API_KEY
import secrets

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)       #Tell FastAPI where to look for the key

def require_api_key(api_key: str = Security(api_key_header)):           #Function that guards the endpoints  
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")  #Raise 401 Error if User doesn't send a key 
    if not secrets.compare_digest(api_key, BOOKS_API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API key")  #Compare the key sent to the real key in the .env file
       
    return api_key                                                      #Passes if theres a match