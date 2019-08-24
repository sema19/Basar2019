'''
Created on 12.06.2019

@author: markus.sedlmeier
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI='sqlite:///db/database.sqlite3'
engine = create_engine(DB_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def Create():
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)        
    
def Remove():
    db_session.remove()
    
        

