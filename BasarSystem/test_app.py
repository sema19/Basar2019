import logging

import connexion
from flask_testing import TestCase
from flask_bootstrap import Bootstrap
#import urllib3
from models import dbModel

class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        #app = connexion.App(__name__, specification_dir='../api/')
        app = connexion.App(__name__, specification_dir='./apispec/',debug=True)
        Bootstrap(app.app)
        app.app.config['TESTING'] = True
        app.app.config['BOOTSTRAP_SERVE_LOCAL'] = True
        app.app.config['LIVESERVER_HOST'] = "0.0.0.0"
        app.app.config['LIVESERVER_PORT'] = 8223
        app.app.config['LIVESERVER_TIMEOUT'] = 10 
        app.add_api('api.yaml')
        #app.add_url_rule('/','/',webpage_ctrl.page_new_version)
        dbModel.Create()
        
        return app.app
    
    #def test_server_is_up_and_running(self):
        #response = urllib2.urlopen(self.get_server_url())
        #self.assertEqual(response.code, 200)
    