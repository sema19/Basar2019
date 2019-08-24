'''
Created on 10.07.2019

@author: markus.sedlmeier
'''

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.schema import ForeignKey
from models.dbModel import Base
from datetime import datetime

class Cart(Base):
    __tablename__="carts"
    id          =   Column(Integer, primary_key=True)
    paydesk_id  =   Column(Integer, ForeignKey("paydesks.id"))    
    status      =   Column(String(200))
    soldtime    =   Column(DateTime) 
    
    
    def __init__(self,
                 paydesk_id=None, 
                 status=None, 
                 soldtime=None          # MAIN, SUPPORT, TOOL       
                 ):               
        self.paydesk_id=paydesk_id                        # where to get the installer
        self.status=status
        self.soldtime=datetime.strptime(soldtime,"%Y-%m-%dT%H:%M:%SZ") if soldtime else None      
                
    def __str__(self):
        return str(self.dump)
            
    def dump(self):
        #return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        retdict={"id":self.id,
                "status":self.status,
                "soldtime":self.soldtime,                
                }        
        return retdict
        
        
