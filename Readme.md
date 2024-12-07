# Book Search API

A simple Flask-based API that provides a book search feature. It allows searching books based on user input, supporting both exact and partial matches. This project includes test cases to ensure the correct functionality of the API.

## Table of Contents
1. [About the Project](#about-the-project)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Testing](#testing)
7. [Contributing](#contributing)

## About the Project

This project is a book search API built using Flask. It allows users to search for books by entering a query string. The API supports the following operations:
- **Search Books**: Allows searching for books by title or partial match.
- **Error Handling**: Returns error messages when the query is empty or no books match the search criteria.

The application is designed to be simple and lightweight, with a focus on testing and API endpoint structure.

## Project Structure

```bash
book-search-api/
├── app.py                  # Main application file
├── models.py               # Data models (if any)
├── tests/                  # Test files for the API
│   ├── test_app.py         # Unit tests for the API
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── venv/                   # Virtual environment (for local development)
```

### Files Explanation:

*   **`app.py`**: Contains the main application code and API endpoints.
*   **`models.py`**: Defines the data models used by the API (if applicable).
*   **`tests/`**: Contains the unit tests for the API endpoints.
*   **`requirements.txt`**: Lists the required Python dependencies.

Installation
------------

### Step 1: Clone the repository

`git clone https://github.com/kunalarya873/better`

`cd better` 

### Step 2: Set up the virtual environment

`python3 -m venv venv`

`source venv/bin/activate`  # On Windows, use 

`venv\Scripts\activate`

### Step 3: Install dependencies

`pip install -r requirements.txt` 

Usage
-----

To run the API, simply start the Flask development server:

`python app.py` 

This will run the API locally on `http://127.0.0.1:5000`.

API Endpoints
-------------

### 1\. **GET /books/search**

Search for books based on a query.

#### Parameters:

*   `query` (required): The search query to search books by.

#### Responses:

*   **200 OK**: A list of books that match the search query.
    *   Example response:
        
        `[
            {
            "title": "Book Title 1",
            "author": "Author Name 1",
            "isbn": "1234567890"
          },
          {
            "title": "Book Title 2",
            "author": "Author Name 2",
            "isbn": "0987654321"
          }
        ]` 
        
*   **400 Bad Request**: Invalid or empty query.
    *   Example response:
        
        `{
          "error": "Empty query"
        }` 
        

#### Example Request:

`GET /books/search?query=python` 

* * *

Testing
-------

To test the application, you can run the unit tests using Python's built-in `unittest` module.

### Step 1: Run tests

`python -m unittest discover tests` 

### Test Cases

*   **`test_search_books_empty_query`**: Tests that an error is returned when the query is empty.
*   **`test_search_books_no_matches`**: Tests that an error is returned when no books match the query.
*   **`test_search_books_partial_match`**: Tests the search functionality for partial matches.

#### Example:

`python -m unittest tests.test_app` 

If everything is set up correctly, you should see output indicating whether the tests pass or fail.

Contributing
------------

We welcome contributions to improve this project. If you want to contribute:

1.  Fork the repository.
2.  Create a new branch.
3.  Make your changes.
4.  Commit and push your changes.
5.  Create a pull request with a description of your changes.

