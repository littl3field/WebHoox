import os
import sys
from pyngrok import ngrok, process
from flask import json
from flask import request
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import hmac
import hashlib

#Define application
application = Flask(__name__)

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
NAME = "RACSN_WebHooks"
CONFIG_PATH = "/Users/%USERNAME%/.ngrok2/ngrok.yml" #Change %USERNAME% to your username
SUBDOMAIN = {
    "subdomain": "CHANGEME" #Change this to whatever domain you require 
}

#Build Ngrok Tunnel
ngrok.connect(port=5000, name=NAME, config_path=CONFIG_PATH, options=SUBDOMAIN)
tunnels = ngrok.get_tunnels()
print(tunnels)

#Verify hash stored in environment variable
def verify_token_hash(data, signature):
    token = bytes(os.environ['WEBHOOK_TOKEN'], 'UTF-8')
    mac_hash = hmac.new(token, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac_hash.hexdigest(), signature)

#Set application route
@application.route('/', methods=['POST'])
def get_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_token_hash(data, signature):
        if request.headers['content-type'] == 'application/json':
            log = json.dumps(request.json)
            with open('logs.json', 'w') as f:
                json.dump(request.json, f)
            return(log)
    else:
        return("Invalid Hash")

#Set logging on application route
@application.route('/')
def error():
    application.logger.warning('A warning occurred (%d total)')
    application.logger.error('An error occurred')
    application.logger.info('Info')
    return(error)

#Run Application
if __name__ == '__main__':
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.run()
