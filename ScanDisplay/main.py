'''
Created on Jul 28, 2019

@author: sedlmeier
'''
'''
Created on Jul 28, 2019

@author: sedlmeier
'''

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from jinja2 import ChoiceLoader, FileSystemLoader

#cfg = configparser.ConfigParser()
#cfg.read('CustomerDisplay.cfg')

#logger = logging.getLogger('log')

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("kasse.html")    

if __name__ == '__main__':
    app.jinja_loader=ChoiceLoader([app.jinja_loader,FileSystemLoader(["views"])])   
    app.run(host="localhost", port=8004, debug=True)
    
