'''
Created on Aug 26, 2018

@author: sedlmeier
'''

import json
import threading
import traceback
import codecs
import socket

import logging

logger = logging.getLogger('sync')



from threading import Event
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import stopAll

# HTTPRequestHandler class
class syncRequestHandler(BaseHTTPRequestHandler):
    
    def log_message(self, *args):        
        pass
        
    def getOkJsonHeader(self):
        self.send_response(200,'OK')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
            
            
    def do_POST(self):
        #logger.debug("POST: %s"%self.path)
        if self.path=="/sync":
            jsonStr=""
            try:
                self.getOkJsonHeader()
                jsonStr = self.getRawData()                
                jsonDataIn=json.loads(jsonStr)                
                paydeskId=jsonDataIn['paydeskId']
                idx=jsonDataIn['idx']
                cnt=jsonDataIn['cnt']
                if 'source' in jsonDataIn:
                    sourcePaydeskId = jsonDataIn['source']
                else:
                    sourcePaydeskId=paydeskId
                ls=LocalStorage()
                
                # add sync request to sync db
                #ls.writeSyncRequestReceived(sourcePaydeskId,idx)
                ret = self.dbWrite("UPDATE paydesks SET lastSyncReqReceived='%s', lastSyncIdx=%d WHERE paydeskId='%s'"%(str(datetime.now()),idx,paydeskId))
                
                items="SELECT * from articles WHERE id>%d ORDER BY id ASC LIMIT %d"%(idx, cnt)
                ret =self.dbQueryAll(stmt)
                
                
                logger.debug("-------- Response to %s: sync sold items: new entries: %s, old index:%s",sourcePaydeskId, str(len(items)),str(idx))
                if len(items)>0:
                    try:
                        logger.debug("Items synced:\n"+"\n".join(items[0]))
                    except Exception as e:
                        logger.error("Not able to show items synced: "+str(e))
                jsonData=json.dumps(items)
                self.wfile.write(jsonData.encode('utf-8'))
                
                
            except json.JSONDecodeError as e:
                logger.error("Invalid json string: %s causes error: %s"%(str(jsonStr),str(e)))
                self.send_response(404)
            except Exception as e:
                logger.error("Error Received Sync: %s"%str(e))
                logger.error(traceback.format_exc())
                self.send_response(404)
            finally:
                del ls
        else:
            self.send_response(404)     
        return

__syncServer__ = None
stopEvent = threading.Event()
isStoppedEvent = threading.Event()

def startSyncWebserver(ip,port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                                      #2 Second Timeout
    result = sock.connect_ex((ip,port))
    if result == 0:
        logger.info('sync port OPEN')
    else:
        logger.info('sync port CLOSED, connect_ex returned: '+str(result))
        
    stopEvent.clear()
    stopAll.AddShutdownEvent(stopEvent)
    
    syncWebserverThread = threading.Thread(name="syncWebserver", target=runSyncWebserver, args=[ip,port])
    syncWebserverThread.start()
    
    syncWebserverObserverThread = threading.Thread(name="syncWebserverObserver", target=syncWebserverObserver)
    syncWebserverObserverThread.start()
    return stopEvent
    
def syncWebserverObserver():
    global __syncServer__
    stopEvent.wait()
    __syncServer__.shutdown()
    
    
def runSyncWebserver(ip, port):
    global __syncServer__
    #ip="127.0.0.1"
    logger.info('start sync server at %s:%d...'%(ip,port))     
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access    
    __syncServer__ = HTTPServer((ip,port), syncRequestHandler)
    logger.info('running sync webserver...')
    __syncServer__.serve_forever()
    logger.info('shutdown sync webserver, closing thread...')
    isStoppedEvent.set()