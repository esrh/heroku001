import os
import urllib
import oauth2 as oauth

def get_request_token(consumer_key, consumer_secret, url):
    authenticate_url = 'https://twitter.com/oauth/authorize'
    request_token_url = 'https://twitter.com/oauth/request_token'
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, url))
    print(content)
    request_token = dict(__parse_qsl(content))
    return '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])

def __parse_qsl(url):
    url = url.decode("utf-8")
    param = {}
    for i in url.split('&'):
        _p = i.split('=')
        param.update({_p[0]: _p[1]})
    return param

def get_access_token(oauth_token, oauth_verifier, consumer_key, consumer_secret):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(oauth_token, oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request("https://api.twitter.com/oauth/access_token",
                                   "POST", body="oauth_verifier={0}".format(oauth_verifier))
    dc = dict(__parse_qsl(content))
    return dc['oauth_token'], dc['oauth_token_secret']



    

