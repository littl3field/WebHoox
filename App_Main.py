import sys
import logging
from flask import json
from flask import request
from flask import Flask
from pyngrok import ngrok, process
from logging.handlers import RotatingFileHandler

#Debug Error Handling for Process Initiation
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

#Defining variables to build Ngrok tunnel
## This overrides the default ngrok config and builds based on params below
NAME = "WebHooks"
CONFIG_PATH = "/Users/%USER%/.ngrok2/ngrok.yml"
SUBDOMAIN = {
    "subdomain": "TESTCHANGEME"
}
ngrok.connect(port=5000, name=NAME, config_path=CONFIG_PATH, options=SUBDOMAIN)
tunnels = ngrok.get_tunnels()
print(tunnels)

app = Flask(__name__)

@application.route('/', methods=['POST'])
def get_payload():
    if request.headers['content-type'] == 'application/json':
        log = json.dumps(request.json)
        with open('logs.json', 'w') as f:
            json.dump(request.json, f)
        return(log)

@app.route('/')
def error():
    app.logger.warning('A warning occurred (%d total)')
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return(error)

if __name__ == '__main__':
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
