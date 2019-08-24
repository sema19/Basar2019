'''
Created on Aug 11, 2019

@author: sedlmeier
'''
# coding: utf-8

from __future__ import absolute_import

from test_app import BaseTestCase
import base64
import json
from datetime import datetime
from datetime import timedelta



class TestCreatePaydesks(BaseTestCase):
    
    paydesklist = [("Kasse1","192.168.2.10",9745,False),
                  ("Kasse2","192.168.2.11",9746,True),
                  ("Kasse3","192.168.2.12",9747,True)]
    
    
    # -------------------------------------------------------------------------
    def test_001(self):     
        """create_paydesks
        """        
        pwp=base64.b64encode(b"basar:teugn")
        for paydesk in self.paydesklist:
            created=datetime.now()-timedelta(hours=30)            
            response = self.client.post(
                '/paydesk',            
                headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
                data=json.dumps({"name":paydesk[0], 
                      "created":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "updated":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "syncIp":paydesk[1],
                      "syncPort":paydesk[2],
                      "remote":paydesk[3],
                      "lastSyncReqReceived":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "lastSyncIdx":0,
                      "itemsSynced":0,                  
                      "lastFailedSyncReq":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "lastFailedSyncCount":1
                      })            
                )            
            retstr=response.data.decode('utf-8')
            self.assert_status(response,201,'Response body is : ' + retstr)
            retObj=json.loads(retstr)
            print(retObj)
        
    
    