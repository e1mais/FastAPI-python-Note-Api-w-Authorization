from xmlrpc.server import DocXMLRPCRequestHandler
from fastapi import FastAPI,status,HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from database import SessionLocal
from typing import List,Optional
import models
from auth.jwt_handler import signJWT
from auth.jwt_Bearer import jwtBearer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#note Schema
class note(BaseModel): 
  id:int
  name:str
  content:str
  class Config:
    orm_mode=True

#note SchemaForSavingPurpouses
class saving_note(BaseModel):
  name:str
  content:str
  class Config:
      orm_mode=True

#user Schema
class user(BaseModel):
  id:int 
  username:str
  password:str
  class Config:
    orm_mode=True

class post_user(BaseModel):
  username:str
  password:str
  class Config:
    orm_mode=True

db = SessionLocal()

@app.get('/', status_code=200)
def welcome_note():
  return "Welcome to my app"


@app.get('/notes', response_model=List[note], status_code=status.HTTP_200_OK)
def get_all_notes():
  notes = db.query(models.Note).all()
  return notes

@app.get('/notes/{id}', response_model=note, status_code=status.HTTP_200_OK)
def get_one_note(id:int):
  note = db.query(models.Note).filter(models.Note.id == id).first()
  return note

@app.post('/notes', dependencies=[Depends(jwtBearer())], response_model=note, status_code=status.HTTP_201_CREATED)
def add_note(body: saving_note): 
  new_note = models.Note(
    name=body.name,
    content=body.content
  )

  existing_note_name = db.query(models.Note).filter(models.Note.name == new_note.name).first()

  if existing_note_name is not None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'El nombre {existing_note_name.name} ya existe')

  db.add(new_note)
  db.commit()

  return new_note
 
@app.put('/notes/{id}', dependencies=[Depends(jwtBearer())], response_model=note, status_code=status.HTTP_202_ACCEPTED)
def modify_note(id:int,body:saving_note):
  existint_note = db.query(models.Note).filter(models.Note.id == id).first()

  if existint_note is not None:
    existint_note.name = body.name
    existint_note.content = body.content

    db.commit()

    return existint_note

  else:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'No se ha encontrado una nota con este identificador {id}') 


@app.delete('/notes/{id}', dependencies=[Depends(jwtBearer())], response_model=note, status_code=status.HTTP_200_OK)
def delete_note(id:int):
  exisiting_note = db.query(models.Note).filter(models.Note.id == id).first()
  
  if exisiting_note is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'No se ha encontrador una nota con este identificador {id}')
    
  db.delete(exisiting_note)
  db.commit()

  return 
  

@app.post('/user/signup', tags=["user"])
def user_signup (user: post_user):
  new_user = models.User(
    username = user.username,
    password = user.password 
  )

  existing_user = db.query(models.User).filter(models.User.username == new_user.username).first()

  if existing_user is not None:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'El nombre de usuario {existing_user.username} no esta disponible')
  
  db.add(new_user)
  db.commit()

  return signJWT(new_user.id)


@app.post('/user/login', tags=['user'])
def user_login (user: post_user):
  is_user = models.User (
    username = user.username,
    password = user.password
  )

  if user_credentials(is_user):
    is_user = db.query(models.User).filter(models.User.username == user.username).first()
    return signJWT(is_user.id)
  
  else:
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail='El nombre de usuario o contraseña son incorrectos')


def user_credentials (user: post_user):
  found_user = db.query(models.User).filter(models.User.username == user.username).first()
  if found_user is not None:
    if found_user.password == user.password:
      return True
  return False