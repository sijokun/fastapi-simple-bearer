from typing import List, Optional, Set, Union

from fastapi import Request, Response
from fastapi.openapi.models import HTTPBearer
from fastapi.security.http import HTTPBase
from pydantic import BaseModel

from fastapi_simple_bearer.exceptions import HeaderNotFound, InvalidHeader, InvalidToken


class FSBToken(BaseModel):
    token: Optional[str] = None


class FSB(HTTPBase):
    def __init__(self, token: str | List[str] | Set[str]):
        self.model = HTTPBearer()
        self.scheme_name = "Bearer Token"

        if isinstance(token, str):
            self._tokens = {token}
        elif isinstance(token, list):
            self._tokens = set(token)
        else:
            self._tokens = token

    def __call__(
        self, req: Request = None, res: Response = None
    ) -> Union[FSBToken, HeaderNotFound, InvalidHeader, InvalidToken]:
        header = req.headers.get("Authorization")
        if not header:
            raise HeaderNotFound()
        if not header.startswith("Bearer "):
            raise InvalidHeader()
        token = header.lstrip("Bearer ")

        if token not in self._tokens:
            raise InvalidToken()

        return FSBToken(token=token)
