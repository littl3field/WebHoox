import logging
from flask import json
from flask import request
from flask import Flask
from logging.handlers import RotatingFileHandler
import json

#Define application 
app = Flask(__name__)

#Set application route 
@app.route('/', methods=['POST'])
def get_payload():
    if (request.headers['content-type'] == 'application/json' and
            request.headers['token'] == 'abc'):
        log = json.dumps(request.json)
        with open('/home/humiologs.json', 'a') as f:
            json.dump(request.json, f)
            f.write("\n")
            return(log)
        f.close()
    else:
        return("Invalid Hash")

#Set logging on application route
@app.route('/')
def error():
    app.logger.warning('A warning occurred (%d total)')
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return(error)

#Run application 
if __name__ == '__main__':
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
