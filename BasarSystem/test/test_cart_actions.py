'''
Created on Aug 13, 2019

@author: sedlmeier
'''

# coding: utf-8

from __future__ import absolute_import

from test_app import BaseTestCase
import base64
import json
from datetime import datetime
from datetime import timedelta



class TestCartActions(BaseTestCase):
    
    articlelist = [("Kasse1","192.168.2.10",9745,False),
                  ("Kasse2","192.168.2.11",9746,True),
                  ("Kasse3","192.168.2.12",9747,True)]
    
    # -------------------------------------------------------------------------
    def test_001_add_to_cart(self):     
        """test add_article to cart
        """        
        pwp=base64.b64encode(b"basar:teugn")        
        response = self.client.post(
            '/cart/add',            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            data=json.dumps({"cart_id":1,"barcode":"123456"})            
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
        
    # -------------------------------------------------------------------------
    '''
    def test_002_closeCart(self):     
        """test close_cart
        """        
        pwp=base64.b64encode(b"basar:teugn")        
        response = self.client.post(
            '/cart/close',            
            headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
            data=json.dumps({"cart_id":1})            
            )            
        retstr=response.data.decode('utf-8')
        self.assert_status(response,200,'Response body is : ' + retstr)
        retObj=json.loads(retstr)
        print(retObj)
    ''' 
        
   
    