from database import Base, engine 
from models import Note


print("Creating database ...")

Base.metadata.create_all(engine)