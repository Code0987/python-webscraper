from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings


class TokenBearer(HTTPBearer):
    '''
    This class is used to authenticate requests using a token.
    It extends the HTTPBearer class from FastAPI and overrides the __call__ method to verify the token.
    For our application, we use a fixed token that is defined in the `.env` file.
    '''

    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(TokenBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify(self, token: str) -> bool:
        return token == settings.AUTH_TOKEN
