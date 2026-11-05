import pytest 

# GET Tests 

def test_get_books_empty(client):       #Ask for all boooks when DB is empty
    response = client.get("/books")     #Send a GET Request to /books using the fake test browser 
    assert response.status_code == 200  #Check that the server said OK
    assert response.json() == []        #Check that the data is returned with an empty list 

def test_get_books_includes_created_book(client, created_book): #Ask for Books when one exists 
    response = client.get("/books")                             #Send GET Request to /books via test browser 
    assert response.status_code == 200                          #Check server said OK 
    assert len(response.json()) == 1                            #Check that list only holds 1 book 
    assert response.json()[0]["title"] == "Test Book"           #Check that book's title matches what we created

def test_get_one_book_real_id(client, created_book):        #Ask for a specifc book using it's ID
    book_id = created_book["id"]                            #Grab the Book ID of the book  created 
    response = client.get(f"/books/{book_id}")              #Put the ID into the URL and ensure GET request was sent 
    assert response.status_code == 200                      #Check server said OK 
    assert response.json()["title"] == "Test Book"          #Check that correct book was returned 

def test_get_one_book_missing_id(client):                   #Ask for book that doesn't exist
    response = client.get("/books/999")                     #Send GET Request 
    assert response.status_code == 404                      #Check server said Error/404
    assert response.json() == {"detail": "Book not found"}  #Check that error message is correct 

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

#PUT Tests 
def test_update_book_success(client, created_book, api_key_headers):    #Successfully update an existing book
    book_id = created_book["id"]                                        #Grab the ID of the book we created in the setup fixture
    response = client.put(                                              #Send a PUT request to update the book
        f"/books/{book_id}",                                            #Put the book's ID into the URL path
        json={"title": "Updated Title", "author": "Updated Author"},    #The new data we want to save
        headers=api_key_headers                                         #Send the valid API key so the server lets us in
    )
    assert response.status_code == 200                          #Check that the server said OK
    assert response.json()["title"] == "Updated Title"          #Check that the response shows the new title
    
    #Confirm with a GET to make sure it actually saved to the database
    get_response = client.get(f"/books/{book_id}")              #Ask the database for this specific book
    assert get_response.json()["title"] == "Updated Title"      #Check that the database now holds the new title

def test_update_book_missing_id(client, api_key_headers):       #Try to update a book that doesn't exist
    response = client.put(                                      #Send a PUT request to a fake ID
        "/books/999",                                           #ID 999 doesn't exist in our empty test database
        json={"title": "Updated", "author": "Updated"},         #Valid data
        headers=api_key_headers                                 #Valid API key
    )
    assert response.status_code == 404                          #Check that the server said Error

#DELETE Tests 
def test_delete_book_success(client, created_book, api_key_headers):            #Successfully delete an existing book
    book_id = created_book["id"]                                                #Grab the ID of the book we created in the setup fixture
    response = client.delete(f"/books/{book_id}", headers=api_key_headers)      #Send a DELETE request with the valid API key
    assert response.status_code == 200                                          #Check that the server said "OK" (200) and returned the deleted book
    
    #Confirm it's actually gone from the database
    get_response = client.get(f"/books/{book_id}")      #Try to GET the book we just deleted
    assert get_response.status_code == 404              #Check that the server says "Not Found" (404) because it's gone

def test_delete_book_twice(client, created_book, api_key_headers):      #Try to delete the same book twice
    book_id = created_book["id"]                                        #Grab the ID of the book we created in the setup fixture
    client.delete(f"/books/{book_id}", headers=api_key_headers)         #First delete: this works perfectly (200)
    
    #Try to delete it again
    response = client.delete(f"/books/{book_id}", headers=api_key_headers)      #Second delete: the book is already gone
    assert response.status_code == 404                                          #Check that the server says Error

#API Key Tests

@pytest.mark.parametrize("method", ["post", "put", "delete"])   #Run this test 3 times (POST, PUT, DELETE)
def test_missing_or_wrong_key(client, created_book, method):    #Test: Try to use write endpoints with bad/missing keys
    book_id = created_book["id"]                                #Grab the ID of the book we created in the setup fixture
    
    #Test 1: No header at all
    if method == "post":    #Testing POST
        response = client.post("/books", json={"title": "X", "author": "Y"})  # Send request WITHOUT the key header
    elif method == "put":   #Testing PUT...
        response = client.put(f"/books/{book_id}", json={"title": "X", "author": "Y"})  # Send request WITHOUT the key header
    else:                   #Testing DELETE...
        response = client.delete(f"/books/{book_id}")  #Send request without the key header
    assert response.status_code == 401  #Check that the server blocked us with a 401 Unauthorized
    
    #Test 2: Wrong key
    bad_headers = {"X-API-Key": "wrong_key"}  # Create a header with a fake, incorrect key
    if method == "post":
        response = client.post("/books", json={"title": "X", "author": "Y"}, headers=bad_headers)
    elif method == "put":
        response = client.put(f"/books/{book_id}", json={"title": "X", "author": "Y"}, headers=bad_headers)
    else:
        response = client.delete(f"/books/{book_id}", headers=bad_headers)
    assert response.status_code == 401  #Check that the server blocked us with an Error
    
    #Test 3: Empty key
    empty_headers = {"X-API-Key": ""}  #Create a header with an empty key
    if method == "post":
        response = client.post("/books", json={"title": "X", "author": "Y"}, headers=empty_headers)
    elif method == "put":
        response = client.put(f"/books/{book_id}", json={"title": "X", "author": "Y"}, headers=empty_headers)
    else:
        response = client.delete(f"/books/{book_id}", headers=empty_headers)
    assert response.status_code == 401  # Check that the server blocked us with a 401 Unauthorized

    #Make sure nothing changed
    #DB Should stay untouched
    get_response = client.get("/books")     #Ask the database for all books
    assert len(get_response.json()) == 1    #Check that there is still exactly 1 book
def test_bad_body_without_key_returns_401(client):  #Send bad data without an API Key
    response = client.post("/books", json={})       #Send POST Request with empty body and no API Key
    assert response.status_code == 401              #Check that server sends a 401 error