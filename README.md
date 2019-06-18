# WebHook_SIEM_Logger

*PLEASE NOTE THIS PROJECT STILL IN DEVELOPMENT*

This is a Python Flask application served by Gunicorn that accepts POST requests inbound from WebHooks. This can be utilised for SOCs to inject logs from services like GitHub, Slack, Bettercloud etc. 

You can run this script from any machine to test web hook collection. This project uses Ngrok to allow for a secure inbound TCP tunnel to a local server for this testing. I recommend that you **DO NOT** use Ngrok for production. Instead, you may want to create a Public Nginx Reverse Proxy or similar on seperate server to send traffic to this application. 

# Features:

* Ngrok intergration development testing of webhook logging to your SIEM
* Store and verify hashed tokens between the service and the application 
* Accept POST Requested in Json format and output to flatfile ready for ingestion to SIEM
* Error logging for system health checks
* Gunicorn Web Server Gateway Interface for production use

### Installation
Close the script:
```sh
$ git clone https://github.com/rylittlefield/WebHook_SIEM_Logger.git
```
TEST"

Install the dependencies and devDependencies and start the server.

```sh
$ cd WebHook_SIEM_Logger
$ pip install -r requirements.txt
```
Set your secret in an environment variable named WEBHOOK_TOKEN
```sh
$ export WEBHOOK_TOKEN="%SECRETTOKEN%"
```

When testing in development environment. Edit your Ngrok yml file located in /Users/%USER%/.ngrok2/ngrok.yml, see https://ngrok.com/docs for details on how to configure the config you need. Here you can add your API key for premium users. Example:
```sh
authtoken: %APIKEY%
region: eu
update: false
update_channel: stable
web_addr: localhost:4040
tunnels:
  humio:
    proto: http
    addr: 5000
    subdomain: test
    inspect: false

```

Gunicorn to run your application...

```sh
$ gunicorn --bind 0.0.0.0:5000 WSGI_Server_Main
```

This project uses port 5000, you can change this by ammending the "port=" variable & above command.

_____

### Running in production 
I recommend using a public facing proxy server for production setups, Ngrok should only be used in testing. Comment out (4DEVENV) sections if you are moving to production.

Once you have commented this out, you should create a systemd service unit for gunicorn - you can do this by looking at this guide here: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

You will then need to allow traffic from the NGINX server on that port:

```sh
firewall-cmd --permanent --add-port=8000/tcp
```
_____

### To Do!

* Argparse 
* Syslog intergration 
*
