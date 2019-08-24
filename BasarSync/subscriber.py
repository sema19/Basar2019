'''
Created on 08.08.2017

@author: Laptop8460
'''

import threading
import time
import traceback
import socket
import json
from sys import platform
from controllers import paydesk_ctrl

import logging
import stopAll

# Logger settings
logger = logging.getLogger('subscription')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("log/subscription.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fmtr = logging.Formatter("%(threadName)s %(asctime)s  %(levelname)s: %(message)s","%H:%M:%S")
ch.setFormatter(fmtr)
logger.addHandler(fh)
logger.addHandler(ch)

#from LocalStorage import LocalStorage
stopAllEvent=threading.Event()

startSubscriptionUpdateEvent=threading.Event()
publishEvent = threading.Event()
subscriberUpdaterDebug = threading.Event()
subscriberSenderStopEvent=threading.Event()
       
broadcastSentEvent=threading.Event()
                     
def startSubscriberUpdater(broadcastPort):    
    # wait for others to subscribe         
    subscriberSender = threading.Thread(name="subscriptionUpdater",
                                        target=runSubscriberUpdater,
                                        args=[broadcastPort])
    subscriberSender.start()
    stopAll.AddShutdownEvent(subscriberSenderStopEvent)
    stopAll.AddShutdownEvent(publishEvent)

def triggerSubscriberUpdater():
    publishEvent.set()
    
def stopSubscriberUpdater():    
    subscriberSenderStopEvent.set()
    publishEvent.set()
    
    
def runSubscriberUpdater(port):
    logger.info("START SUBSCRIBER UPDATER TO PORT %s"%(str(port)))
    subscriberSenderStopEvent.clear()
    broadcastSendCnt=0
    triggerTxt=""        
    while(True):        
        #logger.debug("SUBSCRIBER UPDATER - WAIT FOR PUBLISH EVENT")
        evRet=publishEvent.wait(30)     # set publish event on new cart sold or after 30 seconds
        if evRet:
            triggerTxt="EVENT"
            #logger.debug("publish event received")
        else:
            triggerTxt="TIMEOUT(30s)"        
        publishEvent.clear()
        publish=True        
        try:
            if publish:                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                #ls = LocalStorage()
                #ret = ls.getLocalPaydesk()
                # get local paydesk
                localpaydesks = paydesk_ctrl.get(remote=0)
                for paydesk in localpaydesks:                
                    if subscriberSenderStopEvent.isSet():
                        logger.debug("send publish broadcast bye!")
                        action="bye"
                    else:                        
                        #logger.debug("-> BROADCAST(%s) %d: SyncInfo:%s, %s:%s"%(triggerTxt,broadcastSendCnt, ret[1],ret[4],str(ret[5])))
                        action="subscribe"                    
                    json_subscribe=json.dumps({"action":action,"paydesk":paydesk.dump()})
                    #if broadcastSendCnt%10:
                    #    logger.debug("Broadcast:"+str(json_subscribe))
                    broadcastSendCnt+=1
                    sock.sendto(str(json_subscribe).encode('utf-8'), ('192.168.2.255', port))     #192.168.255.255
                    broadcastSentEvent.set()
                    
                else:
                    logger.debug("subscription update failed - no paydesk received")
                #del ls
        except:
            logger.error(traceback.format_exc())
        
        if subscriberSenderStopEvent.isSet():
            subscriberSenderStopEvent.clear()
            # that late to be able to say good bye with broadcast
            logger.info("STOP SUBSCRIBER UPDATER")
            break    
                