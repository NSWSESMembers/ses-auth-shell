#!/usr/bin/env python3

import sys, os
from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

BASE_URL = 'https://identitypreview.ses.nsw.gov.au/'

try:
    app_id = os.environ['APP_ID']
    app_secret = os.environ['APP_SECRET']
except KeyError:
    print('Please specify APP_ID and APP_SECRET environment variables.',
          file=sys.stderr)

oauth_client = oauth.remote_app(
    'ses',
    consumer_key=app_id,
    consumer_secret=app_secret,
    request_token_params={
        'scope': 'openid profile beaconApi',
    },
    base_url=BASE_URL,
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'{BASE_URL}core/connect/token',
    authorize_url=f'{BASE_URL}core/connect/authorize',
)


@app.route('/')
def index():
    if 'oauth_token' in session:
        me = oauth_client.get('https://apipreviewbeacon.ses.nsw.gov.au/Api/v1/Users')
        return jsonify(me.data)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback_url = url_for('authorized', _external=True)
    print(callback_url)
    return oauth_client.authorize(
        callback=callback_url,
    )


@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
      resp = oauth_client.authorized_response()
      if resp is None or resp.get('access_token') is None:
          return 'Access denied: reason=%s error=%s resp=%s' % (
              request.args['error'],
              request.args['error_description'],
              resp
          )
      session['oauth_token'] = (resp['access_token'], '')
      return redirect(url_for('index'))


@oauth_client.tokengetter
def get_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
