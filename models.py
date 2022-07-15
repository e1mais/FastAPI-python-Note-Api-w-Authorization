from sqlalchemy import String, Integer, Column, Text 
from database import Base

#Schema 
class Note(Base):
  __tablename__ = 'note'
  id = Column(Integer,primary_key=True)
  name=Column(String(25),nullable=False,unique=True)
  content=Column(Text)

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  username=Column(String(25),nullable=False,unique=True)
  password=Column(String(255),nullable=False)

