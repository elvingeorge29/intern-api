def test_get_books_empty(client):           #Test; pytest run the client setup 
    response = client.get("/books")         #Send a GET Request to the /books URL and save the server's reply in a variable called "response"
    assert response.status_code == 200      #Server reply with a 200 OK status 
    assert response.json() == []            #Expect the data sent back to be an empty list