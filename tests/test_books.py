import pytest 

# GET Tests 

def test_get_books_empty(client):       #Ask for all boooks when DB is empty
    response = client.get("/books")     #Send a GET Request to /books using the fake test browser 
    assert response.status_code == 200  #Check that the server said OK
    assert response.json() == []        #Check that the data is returned with an empty list 

def test_get_books_includes_created_book(client, created_book): #Ask for Books when one exists 
    response = client.get("/books")         #Send GET Request to /books via test browser 
    assert response.status_code == 200      #Check server said OK 
    assert len(response.json()) == 1        #Check that list only holds 1 book 
    assert response.json()[0]["title"] == "Test Book"       #Check that book's title matches what we created

def test_get_one_book_real_id(client, created_book):        #Ask for a specifc book using it's ID
    book_id = created_book["id"]                            #Grab the Book ID of the book  created 
    response = client.get(f"/books/{book_id}")              #Put the ID into the URL and ensure GET request was sent 
    assert response.status_code == 200                      #Check server said OK 
    assert response.json()["title"] == "Test Book"          #Check that correct book was returned 

def test_get_one_book_missing_id(client):               #Ask for book that doesn't exist
    response = client.get("/books/999")                 #Send GET Request 
    assert response.status_code == 404                  #Check server said Error/404
    assert response.json() == {"detail": "Book not found"}  #Ensure that error message is correct 

def test_get_one_book_invalid_id(client):               #Check for book using text instead of a number 
    response = client.get("/books/abc")                 #Send GET Request to /books
    assert response.status_code == 422                  #Check that server returned a 422 error 

# POST tests 

def test_create_book_success(client, api_key_headers):      #Create a New Book 
    response = client.post(                                 #POST Request to create a book 
        "/books",                                           #URL Being used
        json={"title": "New Book", "author": "New Author"}, #Data to send in the Request Body 
        headers=api_key_headers                             #Headers that contains the correct API Key 
    )
    assert response.status_code == 201                      #Check that server said Created
    data = response.json()                                  #Save the JSON response in a variable
    assert isinstance(data["id"], int)                      #Check that new ID is a number/int
    assert data["title"] == "New Book"                      #Check that title matches what was sent

def test_create_book_appears_in_db(client, api_key_headers):            #Make sure the new book is actually saved 
    client.post("/books", json={"title": "Check DB", "author": "Author"}, headers=api_key_headers)  #Create a Book 
    response = client.get("/books")                                     #Ask DB for All books 
    assert len(response.json()) == 1                                    #Check that there is 1 book in the list 
    assert response.json()[0]["title"] == "Check DB"                    #Check that it is the exact book created 

#POST Bad Data Sets 

@pytest.mark.parametrize("bad_payload", [           #Run test with different bad data 
    {"title": "", "author": "Author"},              #Empty title
    {"title": "Title", "author": ""},               #Empty author
    {"title": "Title"},                             #Missing author
    {"author": "Author"},                           #Missing title
    {"title": 123, "author": "Author"},             #Wrong type (number)
    {}                                              #Empty body
])
def test_create_book_bad_data(client, api_key_headers, bad_payload):            #Try to create book with bad data 
    response = client.post("/books", json=bad_payload, headers=api_key_headers) #Send the bad data
    assert response.status_code == 422                                          #Check that server rejected it with 422 error 
    get_response = client.get("/books")                                         #Ask DB for All books
    assert len(get_response.json()) == 0                                        #Ensure nothing was created