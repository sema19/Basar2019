'''
Created on Aug 2, 2019

@author: sedlmeier
'''

from sqlalchemy import Column, String, Integer, DateTime
from models.dbModel import Base
from datetime import datetime

class Seller(Base):
    __tablename__="sellers"
    id          =   Column(Integer, primary_key=True)    
    number      =   Column(String(200))
    code        =   Column(String(200)) 
    firstname   =   Column(String(200))
    lastname    =   Column(String(200))
    phone       =   Column(String(200))
    created     =   Column(DateTime)
    email       =   Column(String(200))
    
    
    def __init__(self, 
                 number=None, 
                 code=None,
                 firstname=None,
                 lastname=None,
                 phone=None,
                 created=None,
                 email=None,       
                 ):       
        self.number=number
        self.code=code       
        self.firstname=firstname
        self.lastname=lastname
        self.phone=phone
        self.created=datetime.strptime(created,"%Y-%m-%dT%H:%M:%SZ") if created else None        
        self.email=email
                
    def __str__(self):
        return str(self.dump)
            
    def dump(self):
        #return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        retdict={"id":self.id,
                "number":self.number,
                "code":self.code,                
                "firstname":self.firstname,
                "lastname":self.lastname,
                "phone":self.phone,
                "email":self.email                
                }        
        return retdict            