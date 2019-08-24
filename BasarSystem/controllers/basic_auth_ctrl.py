'''
Created on 03.07.2019

#!/usr/bin/env python3

@author: markus.sedlmeier
'''

import configparser

settings = configparser.ConfigParser()
settings.read("config.ini")

def basic_auth(username, password, required_scopes=None):
    un=settings.get("auth","user")
    pw=settings.get("auth","password")
    if username == un and password == pw:
        info = {'sub': un, 'scope': 'secret'}
    else:
        return None
    
    return info




