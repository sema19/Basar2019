# coding: utf-8

from __future__ import absolute_import

from test_app import BaseTestCase
import base64
import json
from datetime import datetime
from datetime import timedelta



class TestCreateArticles(BaseTestCase):
    
    articlelist = [
        {"seller_id":1, "number":1, "barcode":"34567811","text": "T-Shirt","size":"xxl","price":"4.50", "comment":"TESTARTICLE"},
        {"seller_id":1, "number":2, "barcode":"34567822","text": "Legot","size":"","price":"8.50", "comment":"TESTARTICLE"},
        {"seller_id":1, "number":3, "barcode":"34567833","text": "Schuhe","size":"8 !/2","price":"7.50", "comment":"TESTARTICLE"},
        {"seller_id":2, "number":4, "barcode":"34567841","text": "t-Shirt","size":"xxl","price":"4.50", "comment":"TESTARTICLE"},
        {"seller_id":2, "number":5, "barcode":"34567851","text": "t-Shirt","size":"xxl","price":"4.50", "comment":"TESTARTICLE"}]
                  
    
    # -------------------------------------------------------------------------
    def test_001(self):     
        """create_articles
        """        
        pwp=base64.b64encode(b"basar:teugn")
        for article in self.articlelist:
            created=datetime.now()-timedelta(hours=30)            
            response = self.client.post(
                '/article',            
                headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
                data=json.dumps(article)            
                )            
            retstr=response.data.decode('utf-8')
            self.assert_status(response,201,'Response body is : ' + retstr)
            retObj=json.loads(retstr)
            print(retObj)
            
    '''
    # -------------------------------------------------------------------------
    def test_001(self):     
        """create_articles
        """        
        pwp=base64.b64encode(b"basar:teugn")
        for article in self.articlelist:
            created=datetime.now()-timedelta(hours=30)            
            response = self.client.post(
                '/article',            
                headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
                data=json.dumps(**article{"seller_id":article["seller_id"], 
                      "number":article["number"],
                      "barcode":article["barcode"],
                      "text":"etwas",
                      "size":"xxl",
                      "price":"4.50",
                      "created":created.strftime("%Y-%m-%dT%H:%M:%SZ"),                  
                      "modified":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "paydesk_id":1,
                      "cart_id":1,
                      "scantime":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "cartstate":0,
                      "comment":"TESTARTICLE"
                      
                      })            
                )            
            retstr=response.data.decode('utf-8')
            self.assert_status(response,201,'Response body is : ' + retstr)
            retObj=json.loads(retstr)
            print(retObj)
    '''