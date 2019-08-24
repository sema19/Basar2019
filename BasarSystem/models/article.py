'''
Created on Aug 2, 2019

@author: sedlmeier
'''
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.schema import ForeignKey 
from models.dbModel import Base
from datetime import datetime

class Article(Base):
    __tablename__="articles"
    id              = Column(Integer, primary_key=True)    
    seller_id       = Column(Integer, ForeignKey("sellers.id"))
    number          = Column(Integer)
    barcode         = Column(String)
    text            = Column(String(500))
    size            = Column(String(100))
    price           = Column(Float)
    created         = Column(DateTime)
    modified        = Column(DateTime)
    #during sale
    sold            = Column(Boolean, default=False)
    paydesk_id      = Column(Integer, ForeignKey("paydesks.id"))    
    cart_id         = Column(Integer, ForeignKey("carts.id"))    
    scantime        = Column(DateTime)
    cartstate       = Column(Integer)            #0=OK, 1=removed
    comment         = Column(String(100))               #comment on status
              
    def __init__(self, 
                 seller_id=None, 
                 number=None,
                 barcode=None,
                 text=None,
                 size=None,
                 price=None,
                 created=None,
                 modified=None,          # MAIN, SUPPORT, TOOL
                 sold=None,
                 paydesk_id=None,
                 cart_id=None,
                 scantime=None,
                 cartstate=None,
                 comment=None                        
                 ):                                       # where to get the installer
        self.seller_id=seller_id 
        self.number=number
        self.barcode=barcode
        self.text=text
        self.size=size
        self.price=float(price)
        self.created=datetime.strptime(created,"%Y-%m-%dT%H:%M:%SZ") if created else None
        self.modified=datetime.strptime(modified,"%Y-%m-%dT%H:%M:%SZ") if modified else None
        self.paydesk_id=paydesk_id
        self.cart_id=cart_id
        self.scantime=datetime.strptime(scantime,"%Y-%m-%dT%H:%M:%SZ") if scantime else None
        self.cartstate=cartstate
        self.comment=comment
                
    def __str__(self):
        return str(self.dump)
            
    def dump(self):
        #return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        retdict={
            "id":self.id,
            "seller_id":self.seller_id, 
            "number":self.number,
            "barcode":self.barcode,
            "text":self.text,
            "size":self.size,
            "price":self.price,
            "created":self.created,
            "modified":self.modified,
            "sold":self.sold,
            "paydesk_id":self.paydesk_id,
            "cart_id":self.cart_id,
            "scantime":self.scantime.strftime("%Y-%m-%dT%H:%M:%SZ") if self.scantime else None,
            "cartstate":self.cartstate,
            "comment":self.comment               
                }        
        return retdict        
        
        
