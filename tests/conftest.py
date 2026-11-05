#Shared Room for all the tests to run
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["BOOKS_API_KEY"] = "test_api_key_123"                #Set the test environment API Key before importing the app
os.environ["DATABASE_URL"] = "postgresql+psycopg2://booksuser:bookspass@localhost:5432/booksdb_test" #Set the test Environment URL before importing the app 

from main import app                        #Import the App 
from database import Base, get_db           #Import the Database

TEST_DB_URL = os.environ["DATABASE_URL"]    #Safely check; makes sure that tests are pointing at the correlating databases
if not TEST_DB_URL.endswith("_test"):       #If it doesn't pass the test, raise error to stop proceeding
    raise RuntimeError("ERROR: Tests must only run against a database ending in '_test'")

test_engine = create_engine(TEST_DB_URL)    #Create the test engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=test_engine)    #Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)  
    yield
    Base.metadata.drop_all(bind=test_engine)    #Drop tables after all tests are done (optional cleanup)


@pytest.fixture(autouse=True)                                   #Run this automatically before every single test 
def clean_db():                                                 #The name/label for this database
    with test_engine.connect() as conn:                         #Before every single test, empty the table
        conn.execute(Base.metadata.tables["books"].delete())    #Run SQL Delete for books table so next test starts with a blank slate
        conn.commit()
    yield

@pytest.fixture
def client():                       #Name of this setup is Client 
    def override_get_db():          #Override the get_db dependency so the app uses the TEST database
        db = TestingSessionLocal()  #Opens connection to the test database 
        try:
            yield db                #Let the database go through for testing 
        finally:                    #Continue on the next line 
            db.close()              #Close the database connection
    
    app.dependency_overrides[get_db] = override_get_db  #When endpoint asks for connection, ignore get_db and use override_get_db
    
    with TestClient(app) as c:      #Give the test the client
        yield c                     #Hand the fake browser to the test
    
    app.dependency_overrides.clear()    #Clear the overrides after the test

@pytest.fixture                                     #Fixture = reusable setup tool
def api_key_headers():                              #Defines the fixture 
    return {"X-API-Key": "test_api_key_123"}        #Returns the headers needed to pass the API Key Check


@pytest.fixture                                                 #Fixture = reusable setup tool 
def created_book(client, api_key_headers):                      #Defines the new fixture while also referencing previous fixtures (client, api_headers)
    response = client.post(                                     #Uses the fake test client to send a POST Request to API 
        "/books",                                               #URL path for the end point
        json = {"title": "Test Book", "author": "Test Author"}, #Body section for the POST endpoint, data to save 
        headers = api_key_headers                               #Passes in the dictionary from the first fixture
    )
    return response.json()                                      #Returns the server's JSON response