import os
import json
import logging
from functools import wraps
from base64 import b64decode
from flask import Flask, g, redirect, abort
from flask_oidc import OpenIDConnect

logging.basicConfig(level=logging.DEBUG)

realm = os.environ['realm']
clientId = os.environ['clientid']
clientSecret = os.environ['clientsecret']
url = os.environ['url']
authority = url + "/realms/" + realm

app = Flask(__name__, static_url_path='',  static_folder='wwwroot')
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': {
        "web": {
            "issuer": authority,
            "auth_uri": authority + "/protocol/openid-connect/auth",
            "client_id": clientId,
            "client_secret": clientSecret,
            "redirect_uris": [
                "http://localhost:8090/*"
            ],
            "userinfo_uri": authority + "/protocol/openid-connect/userinfo", 
            "token_uri": authority + "/protocol/openid-connect/token",
            "token_introspection_uri": authority + "/protocol/openid-connect/token/introspect",
            "bearer_only": "true"
        }
    },
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'    
})
oidc = OpenIDConnect(app)

data = [
  {"id":1,"value":"1"},
  {"id":2,"value":"2"},
  {"id":3,"value":"3"},
  {"id":4,"value":"4"}
]

def require_keycloak_role(client, role):
    def wrapper(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            pre, tkn, post = oidc.get_access_token().split('.')
            access_token = json.loads(b64decode(tkn + "==="))
            if role in access_token['resource_access'][client]['roles']:
                return view_func(*args, **kwargs)
            else:
                return abort(403)
        return decorated
    return wrapper

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/login')
@oidc.require_login
def login():
    return redirect('/')

@app.route('/logout')
def logout():
    ''' 
    Logout has an issue where it doesnt support SSO logout at this point:
    https://github.com/puiterwijk/flask-oidc/issues/5#issuecomment-86187023
    '''
    oidc.logout()
    return redirect('/')

@app.route('/state')
def state():
    return json.dumps({'authenticated': oidc.user_loggedin})

@app.route('/token')
@oidc.require_login
def token():
    if oidc.user_loggedin:    
        return json.dumps({'token': oidc.get_access_token()})
    else:
        return abort(403)

@app.route('/api/Values/<id>', methods=['GET'])
@oidc.accept_token(require_token=True)
def value(id):
    return json.dumps({id: id})

@app.route('/api/Values',  methods=['GET'])
@oidc.accept_token(require_token=True)
@require_keycloak_role('demo-app-authorization', 'Administrator')
def values():
     return json.dumps(data)     

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8090')