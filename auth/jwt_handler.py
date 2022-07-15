#
from cmath import exp
import time
from unittest import expectedFailure 
import jwt 
from decouple import config


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

def response_token (token: str):
  return {
    "access token" : token
  }

def signJWT(userId: str):
  payload = {
    "userId": userId,
     "expiry": time.time() + 800
  }

  token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
  return response_token(token)

def decodeJWT(token:str):
  try:
    decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return decode_token if decode_token['expires'] >= time.time() else None
  except:
    return {}