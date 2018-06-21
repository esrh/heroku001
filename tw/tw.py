from flask import (Blueprint, render_template, request, redirect,
  session, make_response, send_file,
  make_response, send_from_directory)
import os, io
from tw import tw_auth
from twitter import *

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

@app.route('/tw/collect')
def collect_tweet_200():
    consumer_key, consumer_secret, hoge = __keys()
    if "oauth_token" not in session:
        return 'need login'
    a, b = session.get('oauth_token', ''), session.get('oauth_token_secret', '')
    t = Twitter(auth=OAuth(a, b, consumer_key, consumer_secret))
    user_id = session.get('oauth_token', '').split('-')[0]
    xc = '"tweet","created_at","source"\n'
    x = None
    for count in range(2):
        if x is not None:
            x = t.statuses.user_timeline(count=200, user_id=user_id, max_id=x[-1]['id'] - 1)
        else:
            x = t.statuses.user_timeline(count=200, user_id=user_id)
        for xx in x:
            xc += '"{}"'.format(xx['text'].replace('"', '""'))
            xc += ',"{}"\n'.format(xx['created_at'].replace('"', '""'))
            xc += ',"{}"\n'.format(xx['source'].replace('"', '""'))
        if x == '':
            break
    bi = io.BytesIO()
    bi.write(xc.encode('utf-8'))
    res = make_response()
    res.data = bi.getvalue()
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    bi.close()
    return res

