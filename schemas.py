from pydantic import BaseModel, Field, ConfigDict

class BookIn(BaseModel):                                    #Defines the shape of the data the client needs to send
    title: str = Field(min_length=1)                        #Title must be a string, min char count of 1 
    author: str = Field(min_length=1)                       #Author must also be a string, min chat count of 1 

    model_config = ConfigDict(
        str_strip_whitespace = True,
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald"
            }
        }
    )
class ErrorResponse(BaseModel):     
    detail: str