import unittest
from app import app

class TestLibraryAPI(unittest.TestCase):
    def setUp(self):
        # Create a test client
        """
        Create a test client and login to get a valid token to use in other tests
        
        Sets up the following instance variables:
        - client: a test client
        - token: a valid token for a test user
        - headers: a dictionary with a valid Authorization header
        """
        self.client = app.test_client()
        self.client.testing = True

        # Login to get a valid token
        login_response = self.client.post('/login', json={"user_id": "test_user"})
        self.assertEqual(login_response.status_code, 200)
        self.token = login_response.json["token"]
        self.headers = {"Authorization": self.token}

    def test_create_user(self):
        # Test user creation
        
        """
        Tests that a user can be created by making a POST request to /login with a
        new user_id.

        Verifies that the response status code is 200 and that the response contains
        a token.
        """
        response = self.client.post('/login', json={"user_id": "new_user"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_create_book(self):
        # Add a new book
        """
        Tests the creation of a new book by making a POST request to the /books endpoint.

        Verifies that the response status code is 201 (Created) and that the response contains
        a success message confirming the addition of the book.
        """
        response = self.client.post('/books', json={
            "title": "Sample Book",
            "author": "John Doe",
            "publication_year": 2021
        }, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Book added")

    def test_get_book_by_id(self):
        # Add a book to retrieve
        """
        Tests retrieving a book by its ID after adding it.

        Verifies that a book can be successfully added and retrieved
        using a GET request to the /books/<book_id> endpoint. Asserts
        that the response status code is 200 and that the retrieved
        book's title matches the expected value.
        """
        add_response = self.client.post('/books', json={
            "title": "Test Book",
            "author": "John Doe",
            "publication_year": 2021
        }, headers=self.headers)
        self.assertEqual(add_response.status_code, 201)

        # Retrieve the book by ID
        book_id = add_response.json["book"]["book_id"]
        response = self.client.get(f'/books/{book_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json)
        self.assertEqual(response.json["title"], "Test Book")

    def test_update_book(self):
        # Add a book to update
        """
        Tests updating a book by its ID after adding it.

        Verifies that a book can be successfully added and updated
        using a PUT request to the /books/<book_id> endpoint. Asserts
        that the response status code is 200 and that the retrieved
        book's title matches the expected value.
        """
        add_response = self.client.post('/books', json={
            "title": "Old Book",
            "author": "Jane Doe",
            "publication_year": 2020
        }, headers=self.headers)
        self.assertEqual(add_response.status_code, 201)

        # Update the book
        book_id = add_response.json["book"]["book_id"]
        response = self.client.put(f'/books/{book_id}', json={
            "title": "Updated Book Title",
            "author": "Jane Doe",
            "publication_year": 2022
        }, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Book updated")

    def test_delete_book(self):
        # Add a book to delete
        """
        Tests deleting a book by its ID after adding it.

        Verifies that a book can be successfully added and deleted
        using a DELETE request to the /books/<book_id> endpoint. Asserts
        that the response status code is 200 and that the retrieved
        book's title matches the expected value.
        """
        add_response = self.client.post('/books', json={
            "title": "Book to Delete",
            "author": "Author",
            "publication_year": 2021
        }, headers=self.headers)
        self.assertEqual(add_response.status_code, 201)

        # Delete the book by ID
        book_id = add_response.json["book"]["book_id"]
        response = self.client.delete(f'/books/{book_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Book deleted")

    def test_search_books_query(self):
        # Add a book for searching
        """
        Tests searching for a book by its title and author.

        Verifies that a book can be added and then successfully found using
        query parameters for title and author. Asserts that the response 
        status code is 200, the search results are not empty, and the 
        title of the first book in the results matches the expected value.
        """

        self.client.post('/books', json={
            "title": "Sample Book",
            "author": "John Doe",
            "publication_year": 2021
        }, headers=self.headers)

        # Search for the book by title and author using query parameters
        response = self.client.get('/books?title=Sample&author=John', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertEqual(response.json[0]["title"], "Sample Book")

    def test_search_books_per_page(self):
        # Add multiple books
        """
        Tests searching for books using pagination by adding two books and verifying that only
        two books are returned in the search results when using pagination.
        """
        self.client.post('/books', json={
            "title": "Book 1",
            "author": "Author",
            "publication_year": 2021
        }, headers=self.headers)
        self.client.post('/books', json={
            "title": "Book 2",
            "author": "Author",
            "publication_year": 2021
        }, headers=self.headers)

        # Search with pagination
        response = self.client.get('/books?page=1&per_page=2', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_search_books_empty_query(self):
        """
        Tests that an error is returned when the query is empty.
        
        Verifies that the response status code is 400 and that the response contains
        an error message.
        """
        response = self.client.get('/books/search?query=')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_search_books_no_matches(self): 
        """
        Tests that an empty list is returned when no books match the query.
        Verifies that the response status code is 200 and that the response contains
        an empty list.
        """
        response = self.client.get('/books/search?query=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)


    def test_search_books_partial_match(self):
        # Add a book with a long title
        """
        Tests that a book can be found using a partial match for its title.

        Verifies that a book can be added and then successfully found using a
        partial match of its title. Asserts that the response status code is 200 and
        that the response contains a success message.
        """
        self.client.post('/books', json={
            "title": "A Very Long and Unique Title",
            "author": "Author Name",
            "publication_year": 2023
        }, headers=self.headers)

        # Search using a partial match
        response = self.client.get('/books/search?query=Unique Title', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Search result", response.json['message'])  


class TestLibrarySearchAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class.

        This method is run before all tests. It sets up a test client for
        the Flask app.
        """
        cls.app = app.test_client()

    def test_search_books_empty_query(self):
        """
        Tests that an error is returned when the query is empty.

        Verifies that the response status code is 400 and that the response contains
        an error message.
        """
        response = self.app.get('/books/search?query=')
        self.assertEqual(response.status_code, 400)
if __name__ == '__main__':
    unittest.main()
