'''
Created on Aug 2, 2019

@author: sedlmeier
'''
        
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from models.dbModel import Base
from datetime import datetime

class Paydesk(Base):
    __tablename__="paydesks"
    id                  = Column(Integer, primary_key=True)    
    name                = Column(String)
    created             = Column(DateTime)
    updated             = Column(DateTime)
    syncIp              = Column(String)
    syncPort            = Column(Integer)
    remote              = Column(Boolean)
    lastSyncReqReceived = Column(DateTime)
    lastSyncIdx         = Column(Integer, default=0)   
    itemsSynced         = Column(Integer, default=0)
    lastFailedSyncReq   = Column(DateTime)
    lastFailedSyncCount = Column(Integer)    
    
    def __init__(self, 
                 name=None,
                 created=None,
                 updated=None,
                 syncIp=None,
                 syncPort=None,
                 remote=None,
                 lastSyncReqReceived=None,       
                 lastSyncIdx=None,
                 itemsSynced=None,
                 lastFailedSyncReq=None,
                 lastFailedSyncCount=None
                 ):            
        self.name=name        
        self.created=datetime.strptime(created,"%Y-%m-%dT%H:%M:%SZ") if created else None                
        self.updated=datetime.strptime(updated,"%Y-%m-%dT%H:%M:%SZ") if updated else None        
        self.syncIp=syncIp
        self.syncPort=syncPort
        self.remote=remote
        self.lastSyncReqReceived=datetime.strptime(lastSyncReqReceived,"%Y-%m-%dT%H:%M:%SZ") if lastSyncReqReceived else None
        self.lastSyncIdx=lastSyncIdx
        self.itemsSynced=itemsSynced
        self.lastFailedSyncReq=datetime.strptime(lastFailedSyncReq,"%Y-%m-%dT%H:%M:%SZ")  if lastFailedSyncReq else None
        self.lastFailedSyncCount=lastFailedSyncCount      
                
    def __str__(self):
        return str(self.dump)
            
    def dump(self):
        #return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        retdict={
            "id":self.id, 
            "name":self.name,
            "created":self.created,
            "updated":self.updated,
            "syncIp":self.syncIp,
            "syncPort":self.syncPort,
            "remote":self.remote,
            "lastSyncReqReceived":self.lastSyncReqReceived,       
            "lastSyncIdx":self.lastSyncIdx,
            "itemsSynced":self.itemsSynced,
            "lastFailedSyncReq":self.lastFailedSyncReq,
            "lastFailedSyncCount":self.lastFailedSyncCount              
            }        
        return retdict        
        
        
