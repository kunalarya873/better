import secrets

# Simple token-based authentication
tokens = {}

def generate_token(user_id):
    """
    Generates a unique token for the given user ID.

    This function creates a random token using a secure
    method and associates it with the specified user ID
    in a token storage dictionary.

    Args:
        user_id: An identifier for the user to associate with the token.

    Returns:
        A unique token string associated with the user ID.
    """

    token = secrets.token_hex(16)
    tokens[token] = user_id
    return token

def validate_token(token):
    """
    Validates the provided token and returns the associated user ID.

    This function checks if the given token exists in the token storage
    dictionary and returns the user ID associated with it.

    Args:
        token: A string representing the token to validate.

    Returns:
        The user ID associated with the token if it is valid, otherwise None.
    """
    return tokens.get(token)
