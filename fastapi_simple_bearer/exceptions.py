from fastapi import HTTPException


class HeaderNotFound(HTTPException):
    """
    An error getting header from a request
    """

    def __init__(
        self, status_code: int = 400, message: str = "Authorization header is required"
    ):
        self.status_code = status_code
        self.detail = message


class InvalidHeader(HTTPException):
    """
    An error invalid header in a request
    """

    def __init__(
        self,
        status_code: int = 400,
        message: str = "Authorization should start with 'Bearer'",
    ):
        self.status_code = status_code
        self.detail = message


class InvalidToken(HTTPException):
    """
    An error invalid token in a request
    """

    def __init__(
        self, status_code: int = 401, message: str = "Provided token is invalid"
    ):
        self.status_code = status_code
        self.detail = message
