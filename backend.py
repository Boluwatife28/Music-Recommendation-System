from flask import Flask, redirect, request, session, url_for
import requests
import os
import secrets
import base64
import hashlib
from urllib.parse import urlencode


app = Flask(__name__)
app.secret_key = os.urandom(24)
# Spotify OAuth Configuration
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
USER_INFO_URL = ''

# Spotify scopes (permissions)
SPOTIFY_SCOPES = ['user-read-email','user-read-private']

@app.route('/')
def home():
    return 'Welcome to My Spotify Integration'

@app.route('/login')
def login():
    # Generate a random code verifier and code challenge
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier

    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()
    session['code_challenge'] = code_challenge

    # Build the authorization URL with PKCE parameters using string concatenation
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
        'scope': 'user-read-private user-read-email',  # Adjust scopes as needed
    })
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Verify the state (if needed)
    state = request.args.get('state')

    # Ensure the state matches the one stored in the session (if you use state)
    if state != session.get('state'):
        return 'State mismatch. Authentication failed.'

    # Exchange the code for an access token using PKCE
    code_verifier = session.get('code_verifier')
    token_url = 'https://accounts.spotify.com/api/token'

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'code_verifier': code_verifier,
    }

    response = requests.post(token_url, data=token_data, auth=(CLIENT_ID, CLIENT_SECRET))

    if response.status_code == 200:
        # Successful authentication
        token_info = response.json()
        access_token = token_info['access_token']

        # Use the access token to make API requests to Spotify
        # ...

        return 'Authentication successful!'
    else:
        return 'Authentication failed. Please try again.'

if __name__ == '__main__':
    app.run(debug=True)
