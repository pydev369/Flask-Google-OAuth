from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='YOUR_CONSUMER_KEY',
    consumer_secret='YOUR_CONSUMER_SECRET',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
)

@app.route('/google-login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google-authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (request.args['error_reason'], request.args['error_description'])
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo').data
    # Here, you can use the user_info to create or update a user account in your app's database.
    # You can also redirect the user to a page that requires authentication.
    return 'Welcome, %s!' % user_info['name']

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run()
