'''
Created on Aug 2, 2019

@author: sedlmeier
'''
from models.cart import Cart as CrudObj
from models.dbModel import db_session
from models.article import Article
from models.cart import Cart
from models.paydesk import Paydesk
from datetime import datetime
import json

from connexion import NoContent


class Exception_InvalidPaydesk(Exception): pass
class Exception_InvalidCart(Exception): pass
class Exception_ArticleDoesNotExist(Exception): pass
class Exception_ArticleAlreadySold(Exception): pass
class Exception_CartIsAlreadyEmpty(Exception): pass
        

# ----------------------------------- cart actions -----------------------------------------------

def opencart(paydesk_id=None):
    try:
        msg={"msgtype":"ERROR","msgid":2,"text":"Attempt to open cart", "info":"unexpected error"}
        if paydesk_id is None:
            raise Exception_InvalidPaydesk()

        dbs=db_session()
        cart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.status=="OPEN").one_or_none()
        if cart==None:
            cart=Cart(paydesk_id=paydesk_id, status="OPEN")
            ret = dbs.add(cart)
            dbs.commit()   
            msg={"msgtype":"INFO","msgid":0,"text":"Cart created", "info":"Cart %d created"%(cart.id)}
        else:
            msg={"msgtype":"INFO","msgid":1,"text":"Cart re-opend", "info":"Cart %d reopend"%(cart.id)}
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==cart.id).order_by(Article.scantime.desc()).all()
        return {"Msg":msg, "Cart":cart.dump(),"Articles":[p.dump() for p in articles]}, 200
    except Exception as ex:
        msg={"msgtype":"ERROR","msgid":0,"text":"Severe Error", "info":""}
        return msg, 400        
    
def add(paydesk_id=None, cart_id=None, barcode=None):    
    try:        
        dbs=db_session()            
        cart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.id==cart_id,Cart.status=="OPEN").one_or_none()        
        if cart==None:
            raise Exception_InvalidCart()            
        article=dbs.query(Article).filter(Article.barcode==barcode).one_or_none()
        if article.paydesk_id==None and article.cart_id==None:
            article.paydesk_id=paydesk_id
            article.cart_id=cart_id
            article.scantime=datetime.now()
            dbs.commit();
            ret=200
            msg={"msgtype":"INFO","msgid":0,"text":"Article added", "info":"Article %s: %s %s added"%(barcode, article.text,article.size)}
        else:
            ret=400
            msg={"msgtype":"ERROR","msgid":0,"text":"Article NOT added", "info":"Article %s: %s %s nod added"%(barcode, article.text,article.size)}
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==cart.id).order_by(Article.scantime.desc()).all()    
        return {"Msg":msg, "Cart":cart.dump(),"Articles":[p.dump() for p in articles]}, ret
    except Exception as ex:
        msg={"msgtype":"ERROR","msgid":0,"text":"Severe Error", "info":""}
        return msg, 400                

def close(paydesk_id=None, cart_id=None):
    try:
        dbs=db_session()
        oldCart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.status=="OPEN").one_or_none()
        oldCart.status="CLOSED"
        msg={"msgtype":"INFO","msgid":0,"text":"Cart closed", "info":"Cart %d closed"%(oldCart.id)}    
        newCart=Cart(paydesk_id=paydesk_id, status="OPEN")
        ret = dbs.add(newCart)
        dbs.commit()    
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==newCart.id).order_by(Article.scantime.desc()).all()        
        return {"Msg":msg, "Cart":newCart.dump(),"Articles":[p.dump() for p in articles]}, 200
    except Exception as ex:
        msg={"msgtype":"INFO","msgid":0,"text":"Cart closed", "info":"Cart %d closed"%(oldCart.id)}
        return {"Msg":msg}, 400

def finalize(paydesk_id=None, cart_id=None):
    try:
        dbs=db_session()      
        cart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.id==cart_id).one_or_none()
        cart.status="FINALIZED"
        dbs.commit()
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==cart_id).order_by(Article.scantime.desc()).all()
        syncQueue.addArticles(articles)
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}
          
        return {"Msg":msg, "Cart":cart.dump(),"Articles":[p.dump() for p in articles]},200    
    except Exception as ex:
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}  
        return {"Msg":msg},400

def clear(paydesk_id=None, cart_id=None):
    try:
        dbs=db_session()
        tnow=datetime.now()
        cart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.id==cart_id,Cart.status=="OPEN").one_or_none()
        dbs.execute("update articles SET paydesk_id=null, cart_id=null")             
        dbs.commit()
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==cart_id).order_by(Article.scantime.desc()).all()
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}  
        return {"Msg":msg, "Cart":cart.dump(),"Articles":[p.dump() for p in articles]},200
    except Exception as ex:
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}  
        return {"Msg":msg},200

def redo(paydesk_id=None, cart_id=None):
    try:
        dbs=db_session()
        tnow=datetime.now()
        cart = dbs.query(Cart).filter(Cart.paydesk_id==paydesk_id,Cart.id==cart_id,Cart.status=="OPEN").one_or_none()
        redoArticle=dbs.query(Article).filter(Article.paydesk_id==paydesk_id, Article.cart_id==cart_id).order_by(Article.scantime.desc()).limit(1).one_or_none()
        redoArticle.paydesk_id=None
        redoArticle.cart_id=None
        dbs.commit()
        articles=dbs.query(Article).filter(Article.paydesk_id==paydesk_id,Article.cart_id==cart_id).order_by(Article.scantime.desc()).all()
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}  
        return {"Msg":msg, "Cart":cart.dump(),"Articles":[p.dump() for p in articles]},200
    except Exception as ex:
        msg={"msgtype":"INFO","msgid":0,"text":"Cart finalized", "info":"Cart %s finalized"%(str(cart_id))}  
        return {"Msg":msg},400
        

# ----------------------------------- CURL -----------------------------------------------

def get(limit=None):
    if (limit==None):
        limit=100
    curr_session=db_session()
    q = curr_session.query(CrudObj)    
    return [p.dump() for p in q][:limit]

def get_id(oid):
    curr_session=db_session()
    q = curr_session.query(CrudObj).where(CrudObj.id==oid).one_or_none()    
    return q.dump()


def post(odata):
    curr_session=db_session()     
    tobj = CrudObj(**odata)    
    curr_session.add(tobj)
    curr_session.commit()
    tobjstr=tobj.dump()
    return tobjstr, 201     #note: tobj.dump() here causes {} return, not sure why?!?


def put(oid, odata):
    curr_session=db_session()
    p = curr_session.query(CrudObj).filter(CrudObj.id == oid).one_or_none()
    odata['id'] = oid
    if p is not None:        
        p.update(**odata)
    else:        
        #testobject_object['created'] = datetime.datetime.utcnow()
        curr_session.add(CrudObj(**odata))
    curr_session.commit()
    curr_session.close()
    return NoContent, (200 if p is not None else 201)


def delete(oid):
    curr_session=db_session()
    testobject = curr_session.query(CrudObj).filter(CrudObj.id == oid).one_or_none()
    if testobject is not None:        
        curr_session.query(CrudObj).filter(CrudObj.id == oid).delete()
        curr_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404




