import os
import json
import logging
from jose import jwt
from base64 import b64decode
from flask import Flask, request, abort
from functools import wraps
from json import dumps

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_url_path='',  static_folder='wwwroot')
app.config.update({
    'TESTING': True,
    'DEBUG': True  
})

realm = os.environ['realm']
clientId = os.environ['clientid']
url = os.environ['url']
authority = url + "/realms/" + realm

data = [
  {"id":1,"value":"1"},
  {"id":2,"value":"2"},
  {"id":3,"value":"3"},
  {"id":4,"value":"4"}
]

def require_keycloak_role(role):
    def wrapper(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            bearer = request.headers['Authorization']
            if bearer == None:
              return abort(403)         
            pre, tkn, post = bearer.split('.')
            access_token = json.loads(b64decode(tkn + "==="))
            if role in access_token['resource_access'][clientId]['roles']:
                return view_func(*args, **kwargs)
            else:
                return abort(403)
        return decorated
    return wrapper

def require_token():
    def wrapper(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            try:
                bearer = request.headers['Authorization']
                if bearer == None:
                  return abort(401)
                token = bearer.strip('Bearer').strip(' ')
                payload = jwt.decode( token, '', options={'verify_signature': False}, audience=clientId, issuer=authority )
                return view_func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return abort(401)
            except jwt.JWTError:
                return abort(401)
        return decorated
    return wrapper    

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/config', methods=['GET'])
def config():
  return json.dumps({"realm": realm, "clientId": clientId, "url": url})

@app.route('/api/Values/<id>', methods=['GET'])
@require_token()
def value(id):
  return json.dumps({id: id})

@app.route('/api/Values',  methods=['GET'])
@require_token()
@require_keycloak_role('Administrator')
def values():
  return json.dumps(data)

if __name__ == '__main__':
     app.run(host="0.0.0.0", port='8090')