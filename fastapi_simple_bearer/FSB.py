from typing import List, Optional, Set, Union

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel


class FSBToken(BaseModel):
    """
    Pydantic model representing a valid bearer token.
    """

    token: str


class FSB(HTTPBearer):
    """
    FastAPI dependency class for simple bearer token authentication.
    """

    def __init__(self, token: Union[str, List[str], Set[str]], auto_error: bool = True):
        """
        Initialize the FSB class with one or multiple valid tokens.

        Args:
            token (Union[str, List[str], Set[str]]): A valid token or a collection of valid tokens.
            auto_error (bool, optional): If True, raises an HTTPException on authentication failure.
                                         Defaults to True.
        """
        super().__init__(auto_error=auto_error)
        if isinstance(token, str):
            self._tokens = {token}
        elif isinstance(token, (list, set)):
            self._tokens = set(token)
        else:
            raise ValueError(
                "Token must be a string, list of strings, or set of strings"
            )

    async def __call__(self, request: Request) -> FSBToken:
        """
        Overrides the __call__ method to perform authentication.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            FSBToken: An instance containing the authenticated token.

        Raises:
            HTTPException: If authentication fails.
        """
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        if not credentials or not credentials.scheme:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials

        if token not in self._tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return FSBToken(token=token)
