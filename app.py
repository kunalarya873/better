from flask import Flask, request, jsonify
from flask.views import MethodView
from models import books, members, Book, Member
from authentication import generate_token, validate_token

app = Flask(__name__)

# Middleware for authentication
from functools import wraps

def authenticate(func):
    """
    Middleware for authentication. Validates the 'Authorization' header
    and returns 401 Unauthorized if invalid. Otherwise, calls the wrapped
    function.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login. Validates the 'user_id' in the request
    and returns a JWT token if valid. Otherwise, returns 400 Bad Request
    if 'user_id' is missing.
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    token = generate_token(user_id)
    return jsonify({"token": token})

# CRUD for Books
@app.route('/books', methods=['POST'])
@authenticate
def add_book():
    """
    Endpoint to add a new book. Requires authentication.

    Expects a JSON payload with book details. The book is assigned 
    a new unique ID and added to the in-memory database. Returns a 
    success message along with the added book details.

    Returns:
        Response: JSON response with a success message and the book 
        details, or an error message if authentication fails.
    """

    data = request.json
    book = Book(book_id=len(books)+1, **data)
    books.append(book)
    return jsonify({"message": "Book added", "book": vars(book)}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
@authenticate
def get_book(book_id):
    """
    Endpoint to get a book by ID. Requires authentication.

    Returns:
        Response: JSON response with book details, or a 404 error if book
        not found.
    """
    book = next((b for b in books if b.book_id == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(vars(book))

@app.route('/books/<int:book_id>', methods=['PUT'])
@authenticate
def update_book(book_id):
    """
    Endpoint to update an existing book by ID. Requires authentication.

    Expects a JSON payload with the fields to update. If the book with the 
    given ID is found, its details are updated and a success message is 
    returned. If no book is found, a 404 error is returned.

    Returns:
        Response: JSON response with a success message and the updated book 
        details, or an error message if the book is not found or authentication 
        fails.
    """

    data = request.json
    book = next((b for b in books if b.book_id == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    for key, value in data.items():
        setattr(book, key, value)
    return jsonify({"message": "Book updated", "book": vars(book)})

@app.route('/books/<int:book_id>', methods=['DELETE'])
@authenticate
def delete_book(book_id):
    """
    Endpoint to delete a book by ID. Requires authentication.

    Removes the book with the specified ID from the in-memory database. 
    Returns a success message if the book is deleted.

    Returns:
        Response: JSON response with a success message, or an error 
        message if authentication fails.
    """

    global books
    books = [b for b in books if b.book_id != book_id]
    return jsonify({"message": "Book deleted"})

# Search and Pagination
@app.route('/books', methods=['GET'])
@authenticate
def list_books():
    """
    Endpoint to list all books with filtering and pagination. Requires authentication.

    Filters books by title and/or author. Accepts the following query parameters:

    - `title`: string, optional, case-insensitive search for books with
      matching title
    - `author`: string, optional, case-insensitive search for books by author
    - `page`: integer, optional, defaults to 1, specifies the page number to
      return
    - `per_page`: integer, optional, defaults to 10, specifies the number of
      books to return per page

    Returns a JSON response with a list of books, each represented as a 
    dictionary with the keys `book_id`, `title`, `author`, and `isbn`.
    """
    title = request.args.get('title')
    author = request.args.get('author')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    filtered_books = books
    if title:
        filtered_books = [b for b in books if title.lower() in b.title.lower()]
    if author:
        filtered_books = [b for b in filtered_books if author.lower() in b.author.lower()]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_books = filtered_books[start:end]

    return jsonify([vars(b) for b in paginated_books])


class BookSearch(MethodView):
    def get(self):
        """
        Handle GET request to search for books.

        Retrieves the 'query' parameter from the request arguments. If the query
        is empty or missing, returns a 400 Bad Request response with an error 
        message. Otherwise, performs a search for books matching the query and 
        returns the search results.

        Returns:
            A JSON response containing either an error message or the search 
            results.
        """

        query = request.args.get('query')
        if not query:
            return jsonify({"error": "Empty query"}), 400
        # Perform the search and return results
        return jsonify({"message": "Search result"})

# Add route conditionally, ensuring it's not registered twice
if not hasattr(app, 'has_routes_added'):
    app.add_url_rule('/books/search', view_func=BookSearch.as_view('search_books'))
    app.has_routes_added = True

if __name__ == '__main__':
    app.run(debug=True)
