from flask import (Blueprint, render_template, request, redirect,
  session, make_response, send_file,
  make_response, send_from_directory)
import os
from tw import tw_auth

app = Blueprint('tw', __name__)

def __keys():
    try:
        key = os.environ['esrh_key']
        s = os.environ['esrh_secret']
        url = 'https://nazotest001.herokuapp.com/tw/callback'
    except:
        with open(os.path.expanduser('~/pass/tw/esrh.txt'), 'r') as f:
            key, s = f.read().split('\n')
        url = 'http://localhost:5000/tw/callback'
    return key, s, url

@app.route('/tw')
def main():
    if "oauth_token" not in session:
        data = 'you need to login'
    else:
        data = 'you are now logged in'
    return render_template('tw.html', data=data, auth_url='tw/login', title='collectmachine')


@app.route('/tw/login')
def login_redirect():
    key, secret, url = __keys()
    return redirect(tw_auth.get_request_token(key, secret, url))

@app.route('/tw/callback', methods=['GET'])
def tw_callback():
    a, b = request.args.get("oauth_token", ""), request.args.get("oauth_verifier", "")
    c, d, hoge = __keys()
    dc = tw_auth.get_access_token(a, b, c, d)
    session['oauth_token'], session['oauth_token_secret'] = dc
    return redirect('/tw') 
