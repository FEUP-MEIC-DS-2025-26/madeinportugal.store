# app.py

from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Flask-Login setup
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OAuth configuration
client_id = 'your_google_client_id'
client_secret = 'your_google_client_secret'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'http://localhost:5000/callback'
scope = ['profile', 'email']


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
        user_info = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
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
    app.run(debug=True)