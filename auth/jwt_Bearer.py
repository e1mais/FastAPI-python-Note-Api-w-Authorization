from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
  def __init__(self, auto_Error : bool = True):
    super(jwtBearer, self).__init__(auto_error=auto_Error)

  async def __call__(self, request: Request):
    credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)

    if credentials:
      if not credentials.scheme == "Bearer":
        raise HTTPException(status_code= 403, detail='La sesión es invalidad')

      return credentials.credentials
    else:
      raise HTTPException(status_code= 403, detail='La sesión es invalida')

  def verify_jwt(self, jwt : str):
    isTokenaizer : bool = False
    payload = decodeJWT(jwt)
    if payload:
      isTokenaizer = True
    return isTokenaizer