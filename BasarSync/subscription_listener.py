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

import logging
import stopAll

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

stopAllEvent=threading.Event()

startSubscriptionUpdateEvent=threading.Event()
publishEvent = threading.Event()
subscriberUpdaterDebug = threading.Event()
subscriberListenerDebug= threading.Event()
subscriberListenerStopEvent = threading.Event()
subscriberSenderStopEvent=threading.Event()
       

def startSubscriberListener(broadcastIp, broadcastPort):
    # start register interface
    subscriberListener = threading.Thread(name="subscriptionService",
                                          target=runSubscriberListener,
                                          args=[broadcastIp,broadcastPort])
    subscriberListener.start()
    stopAll.AddShutdownEvent(subscriberListenerStopEvent)   # triggers a stop
    stopAll.AddShutdownEvent(publishEvent)      # triggers a send
    

def runSubscriberListener(ip,port):
    subscriberListenerStopEvent.clear()
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    if platform=="linux" or platform=="linux2":
        ipa=ip.split('.')[0:3]
        ipa.append('255')
        sock.bind(('.'.join(ipa), port))
        logger.info("START SUBSCRIBER LISTENER AT %s:%s (LINUX:%s)"%(str(ip),str(port),str(ipa)))
    else:
        sock.bind((ip, port))
        logger.info("START SUBSCRIBER LISTENER AT %s:%s (WINDOWS)"%(str(ip),str(port)))    
    while True:
        # wait for message
        #logger.debug("Wait for receive")
        recv,info = sock.recvfrom(1024)
        if subscriberListenerStopEvent.isSet():
            subscriberListenerStopEvent.clear()
            logger.info("STOP SUBSCRIBER LISTENER")
            break
            
        #logger.debug("RECEIVED from %s:%s Data:%s"%(str(info[0]),str(info[1]), str(recv) ))        
        if info[0]==ip:
            # own broadcast
            #logger.debug("OWN BROADCAST RECEIVED from %s:%s Data:%s"%(str(info[0]),str(info[1]), str(recv) ))
            if not broadcastSentEvent.isSet():
                logger.error("Error: own broadcast was not received")
            broadcastSentEvent.clear()
        else:
            jsonData = json.loads(recv.decode())
            action=jsonData["action"]
            paydeskObj=jsonData["paydesk"]
            paydesk = paydesk_ctrl.post(paydeskObj)
        
        
