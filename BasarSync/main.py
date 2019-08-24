'''
Created on Aug 18, 2019

@author: sedlmeier
'''


import logging
import configparser

import connexion
from flask_bootstrap import Bootstrap
from jinja2 import ChoiceLoader, FileSystemLoader
from controllers import webpage_ctrl

from models import dbModel

settings = configparser.ConfigParser()
settings.read("config.ini")
logging.basicConfig(level=logging.INFO)



def main():
    logging.info("--------- START Basar Syncm -------------")
    global application    
    app = connexion.App(__name__, specification_dir='./apispec/',debug=True)
    Bootstrap(app.app)
    app.app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    
    app.app.jinja_loader=ChoiceLoader([app.app.jinja_loader,FileSystemLoader(["views"])])   

    app.add_api('api.yaml')
    #app.add_url_rule('/','/',webpage_ctrl.page_new_version)
    application=app.app
    
    host=settings.get("webserver","host")
    port=settings.get("webserver","port")
    debugflag=settings.getboolean("webserver","debug")
    
    dbModel.Create()
    
    if settings.get("webserver","secure")=="adhoc":
        app.run(host=host, port=port, debug=debugflag, ssl_context='adhoc')
    else:
        app.run(host=host, port=port, debug=debugflag)
    
if __name__ == '__main__':
    main()