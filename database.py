from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_CONNECTION_STRING = "postgresql://postgres:awesomepass@localhost/notes"

engine = create_engine(SQL_CONNECTION_STRING, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)