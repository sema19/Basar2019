'''
Created on Aug 2, 2019

@author: sedlmeier
'''
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.schema import ForeignKey 
from models.dbModel import Base
from datetime import datetime

class Article(Base):
    __tablename__="articles"
    id              = Column(Integer, primary_key=True)            
    barcode         = Column(String)
                  
    def __init__(self,                  
                 barcode=None                        
                 ):                                       # where to get the installer        
        self.barcode=barcode
                        
    def __str__(self):
        return str(self.dump)
            
    def dump(self):
        #return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        retdict={
            "id":self.id,        
            "barcode":self.barcode
            }        
        return retdict        
        
        
