# coding: utf-8

from __future__ import absolute_import

from test_app import BaseTestCase
import base64
import json
from datetime import datetime
from datetime import timedelta

from models.dbModel import db_session
from models.paydesk import Paydesk


class TestScanProcess(BaseTestCase):
    
    paydesk_id=None
    cart_id=None
    
    def setup(self):
        print("is this executed?")
               
    # -------------------------------------------------------------------------
    def test_001_open(self):     
        """create_articles
        """        
        pwp=base64.b64encode(b"basar:teugn")        
        created=datetime.now()-timedelta(hours=30)
        dbs=db_session()        
        paydesk=dbs.query(Paydesk).filter(Paydesk.remote==0).one_or_none()        
        dbs.execute("update articles SET paydesk_id=null, cart_id=null")
        dbs.commit()
        dbs.close()
        
        self.paydesk_id=1   #str(paydesk.id)
                         
        # OPEN CART
                   
        response = self.client.post(
            '/cart/open?paydesk_id=%s'%(str(self.paydesk_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        self.cart_id=retObj["Cart"]["id"]
        print(retObj)
        
        # ADD ARTICE 1
        
        url='/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567833'%(str(self.paydesk_id),str(self.cart_id))        
        response = self.client.post(
            url,            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # ADD ARTICE 2
        
        response = self.client.post(
            '/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567841'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # REDO
        
        response = self.client.post(
            '/cart/redo?paydesk_id=%s&cart_id=%s'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # ADD AGAIN ARTICLE 2
        
        url='/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567841'%(str(self.paydesk_id),str(self.cart_id))        
        response = self.client.post(
            url,            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # CLEAR
        response = self.client.post(
            '/cart/clear?paydesk_id=%s&cart_id=%s'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        
        # ADD AGAIN ARTICE 1
        
        url='/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567833'%(str(self.paydesk_id),str(self.cart_id))        
        response = self.client.post(
            url,            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # ADD AGAIN ARTICE 2
        
        response = self.client.post(
            '/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567841'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # CLOSE CART
        
        response = self.client.post(
            '/cart/close?paydesk_id=%s&cart_id=%s'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        # FINALIZE CART
        
        response = self.client.post(
            '/cart/finalize?paydesk_id=%s&cart_id=%s'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)        
        
        
    
    '''    
    # -------------------------------------------------------------------------
    def test_002_add(self):     
        """create_articles
        """        
        pwp=base64.b64encode(b"basar:teugn")        
        created=datetime.now()-timedelta(hours=30)
        url='/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567833'%(str(self.paydesk_id),str(self.cart_id))        
        response = self.client.post(
            url,            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,201,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        
        
        

           
    # -------------------------------------------------------------------------
    def test_002_add_second(self):     
        """create_articles
        """
                
        pwp=base64.b64encode(b"basar:teugn")        
        created=datetime.now()-timedelta(hours=30)
                
        response = self.client.post(
            '/cart/add?paydesk_id=%s&cart_id=%s&barcode=34567841'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,201,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
        
    # -------------------------------------------------------------------------
    def test_003_close(self):     
        """create_articles
        """        
        pwp=base64.b64encode(b"basar:teugn")        
        created=datetime.now()-timedelta(hours=30)
                                            
        #close cart
        response = self.client.post(
            '/cart/close?paydesk_id=%s&cart_id=%s'%(str(self.paydesk_id),str(self.cart_id)),            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,201,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
    ''' 
   