from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
url = URL(
    drivername = "postgresql",
    username = "postgres",
    password = "postgres.",
    host = "localhost",
    database = "fastapiDB",
    port = 5432
)'''

url_database = 'postgresql://postgres:test1234@localhost:5432/fastapiDB'

engine = create_engine(url_database)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session
Base = declarative_base()