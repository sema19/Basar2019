'''
Created on Aug 2, 2019

@author: sedlmeier
'''
from models.paydesk import Paydesk as CrudObj
from models.dbModel import db_session

from connexion import NoContent

def sync(oid):
    params=json.dumps({'source':localPaydeskId,'paydeskId':paydeskId,'idx':paydeskCnt,'cnt':50}).encode()    
    return syncarticles,201

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



