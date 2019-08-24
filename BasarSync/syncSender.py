'''
Created on Aug 26, 2018

@author: sedlmeier
'''

import requests
import json
import threading
import traceback
from datetime import datetime

from threading import Event
localSyncEvent = threading.Event()
localSyncStopEvent = threading.Event()

import stopAll


# ---------------------------------------------------------------------------  
def updatePaydesk(paydesk):
    ''' Update sold items with all sold items of other playdesks    
    '''
    paydeskId=paydesk[0].strip("\n\r\t ")
    syncIp=paydesk[4].strip("\n\r\t ")
    syncPort=paydesk[5]
    
    localPaydeskId = localPaydesk[0]            
        
    try:
        params=json.dumps({'source':localPaydeskId,'paydeskId':paydeskId,'idx':paydeskCnt,'cnt':50}).encode()
        headers={'content-type':u'application/json'}
        #logger.debug("Request remote paydesk data: URL: "+str(url)+", Data: PaydeskCnt:"+str(paydeskCnt))
        requestTime = datetime.now()
        # request updated items from remote machine
        url = "http://%s:%d/sync"%(paydesk.syncIp,paydesk.syncPort)        
        r=requests.post(url, data=params, headers=headers)
        items=json.loads(r.text)         # r.text holds the payload data
        #build sql
        
                
        #ls.addRemoteSoldItems(items)
        #ls.writeSyncRequest(paydeskId,len(items))
    except requests.exceptions.ConnectionError as e:                
        logger.debug("Connection refused to %s:%s"%(str(syncIp),str(syncPort)))        
        #ls.writeFailedSyncRequest(paydeskId, requestTime)
    except Exception as e:
        logger.error(str(e))

# ---------------------------------------------------------------------------
def startLocalSync():
    global localSyncEvent
    global localSyncStopEvent    
    
    localSyncThread = threading.Thread(name="localSync",target=runLocalSync,
                                       args=[localSyncEvent,localSyncStopEvent])
    localSyncThread.start() 
    stopAll.AddShutdownEvent(localSyncStopEvent)
    stopAll.AddShutdownEvent(localSyncEvent)   
    return localSyncStopEvent
        
# ---------------------------------------------------------------------------        
def runLocalSync(syncEvent, stopEvent):    
    ''' Run through remote paydesks and get the latest articles
    '''    
    logger.info("start local sync thread")
    localSyncStopEvent.clear()
    
    while(1):
        ev = localSyncEvent.wait(10)        
        if ev:
            logger.info("local sync by event")
        localSyncEvent.clear()
        if localSyncStopEvent.isSet():
            localSyncStopEvent.clear()
            logger.info("local sync stop")
            break
        
        try:
            # get items
            ls = LocalStorage()                    
            paydesks=ls.getRemotePaydesks()
            del ls            
            if len(paydesks)>0:
                if paydesks==None:
                    raise Exception("no paydesks found")
                
                logger.debug("-------- iterate through remote paydesks (%d)"%len(paydesks))        
                for paydesk in paydesks:
                    try:
                        updatePaydesk(paydesk)
                    except:
                        logger.error(traceback.format_exc())
                        
        except Exception as e:
            logger.error(e)
            
        
# ---------------------------------------------------------------------------
def triggerLocalSync():
    global localSyncEvent
    logger.debug("trigger local sync event")
    localSyncEvent.set()
    
# ---------------------------------------------------------------------------
def stopLocalSync():
    global localSyncEvent
    global localStopEvent
    logger.info("set stop local sync event")
    localSyncStopEvent.set()
    localSyncEvent.set()  
    
    

