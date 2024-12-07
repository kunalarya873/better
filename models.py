# In-memory database simulation
books = []
members = []

# Data model for Books
class Book:
    def __init__(self, book_id, title, author, publication_year):
        """
        Constructor for Book class.
        
        :param book_id: Unique identifier for the book.
        :param title: Title of the book.
        :param author: Author of the book.
        :param publication_year: Year the book was published.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publication_year = publication_year

# Data model for Members
class Member:
    def __init__(self, member_id, name, email):
        """
        Constructor for Member class.
        
        :param member_id: Unique identifier for the member.
        :param name: Name of the member.
        :param email: Email address of the member.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
