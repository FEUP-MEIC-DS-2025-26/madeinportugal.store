# main.py

import os
import json

from flask import Flask, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Flask-Login setup
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





# OAuth configuration
# Judging by the URLs, this example uses Google OAuth2
# will be replaced with actual client ID, secret and URLs from Jumpseller OAuth settings
def load_client_secret(path='client_secret.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            web = data.get('web', {})
            return {
                'GOOGLE_CLIENT_ID': web.get('client_id'),
                'GOOGLE_CLIENT_SECRET': web.get('client_secret'),
                'AUTHORIZATION_BASE_URL': web.get('auth_uri'),
                'TOKEN_URL': web.get('token_uri'),
                # opcional: usa o primeiro javascript_origin como host de redirect se quiser
                'REDIRECT_HOST': (web.get('javascript_origins') or [None])[0],
            }
    except Exception:
        return {}

# carrega do JSON montado se necessário
json_vals = load_client_secret(os.getenv('CLIENT_SECRET_PATH', 'client_secret.json'))

client_id = os.getenv('GOOGLE_CLIENT_ID') or json_vals.get('GOOGLE_CLIENT_ID') or 'your_google_client_id'
client_secret = os.getenv('GOOGLE_CLIENT_SECRET') or json_vals.get('GOOGLE_CLIENT_SECRET') or 'your_google_client_secret'
authorization_base_url = os.getenv('AUTHORIZATION_BASE_URL') or json_vals.get('AUTHORIZATION_BASE_URL') or 'https://accounts.google.com/o/oauth2/auth'
token_url = os.getenv('TOKEN_URL') or json_vals.get('TOKEN_URL') or 'https://accounts.google.com/o/oauth2/token'

# Construção flexível do redirect_uri
redirect_uri = os.getenv('REDIRECT_URI')
if not redirect_uri:
    redirect_host = os.getenv('REDIRECT_HOST') or json_vals.get('REDIRECT_HOST') or 'https://localhost'
    redirect_port = os.getenv('REDIRECT_PORT', '5000')
    redirect_path = os.getenv('REDIRECT_PATH', '/callback')
    redirect_host = redirect_host.rstrip('/')
    redirect_path = '/' + redirect_path.lstrip('/')
    redirect_uri = f"{redirect_host}:{redirect_port}{redirect_path}"

scope = os.getenv('OAUTH_SCOPE', 'profile email').split()

# Exemplo: imprime para verificação (remova em produção)
print("CLIENT_ID:", client_id)
print("REDIRECT_URI:", redirect_uri)

class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.route('/')
def index():
    if 'google_token' in session:
        oauth = OAuth2Session(client_id, token=session['google_token'])
        user_info = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        return f'Logged in as {user_info["email"]}<br><a href="/logout">Logout</a>'
    return 'You are not logged in<br><a href="/login">Login</a>'


@app.route('/login')
def login():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    google = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = google.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    session['google_token'] = token
    return redirect(url_for('.index'))


@app.route('/logout')
@login_required
def logout():
    session.pop('google_token', None)
    return redirect(url_for('.index'))

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    use_ssl = os.getenv('USE_SSL', 'adhoc').lower()  # '', 'adhoc' ou 'cert'
    # porta padrão: 5000 sem SSL, 443 com SSL por cert
    port = int(os.getenv('PORT', '5000'))
    ssl_context = None

    if use_ssl == 'adhoc':
        # Gera certificado temporário (útil para dev)
        ssl_context = 'adhoc'
        # opcional: permita sobrescrever porta SSL
        port = int(os.getenv('SSL_PORT', os.getenv('PORT', '5000')))
    elif use_ssl == 'cert':
        cert_path = os.getenv('SSL_CERT_PATH', 'cert.pem')
        key_path = os.getenv('SSL_KEY_PATH', 'key.pem')
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            raise SystemExit(f"SSL cert/key não encontrados: {cert_path}, {key_path}")
        ssl_context = (cert_path, key_path)
        port = int(os.getenv('SSL_PORT', '443'))

    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() in ('1', 'true')
    app.run(host=host, port=port, debug=debug_mode, ssl_context=ssl_context)


