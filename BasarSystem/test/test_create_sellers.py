# coding: utf-8

from __future__ import absolute_import

from test_app import BaseTestCase
import base64
import json
from datetime import datetime
from datetime import timedelta



class TestCreateSellers(BaseTestCase):
    
    sellerlist = [("1","1","Hans","Maier","09405/1234", "hans.meier@prodiver.de"),
                  ("2","2","Franz","Huber","09405/1236", "franz.huber@prodiver.de"),
                  ("3","3","Thomas","Müller","09405/1237", "thomas.müller@prodiver.de"),
                  ("4","4","Erwin","Alt","09405/1238", "erwin.alt@prodiver.de")]
    
    # -------------------------------------------------------------------------
    def test_001(self):     
        """create_serllers
        """        
        pwp=base64.b64encode(b"basar:teugn")
        for seller in self.sellerlist:
            created=datetime.now()-timedelta(hours=30)
            response = self.client.post(
                '/seller',            
                headers={"Content-type":"application/json", "Authorization": "Basic "+pwp.decode('utf-8')},
                data=json.dumps({"number":seller[0], 
                      "code":seller[1],
                      "firstname":seller[2],
                      "lastname":seller[3],
                      "phone":seller[4],
                      "created":created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "email":seller[5]                  
                      })            
                )            
            retstr=response.data.decode('utf-8')
            self.assert_status(response,201,'Response body is : ' + retstr)
            retObj=json.loads(retstr)
            print(retObj)
        
    
    