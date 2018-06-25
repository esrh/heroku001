from flask import (Blueprint, Response, render_template, request)
import os, sys, time, json
import requests as rq
import pandas as pd

app = Blueprint('metro', __name__)

def __key():
    try:
        key = os.environ['metro']
    except:
        with open(os.path.expanduser('~/pass/token.json'), 'r') as f:
            key = json.load(f)['metro']
    return key

def __route_table(route):
    df = pd.read_csv('metro/route_table.csv')
    for i, row in df.iterrows():
        if row['route'] == route:
            return row['ID']
    raise

@app.route('/metro/', methods=['GET'])
def metro_mainpage():
    route = request.args.get("metro-line", None)
    sta = request.args.get("metro-station", None)
    if route is None and sta is None:
        rt = ''
    elif sta is None:
        rt = __stations(route)
    elif route is None:
        rt = ''
    else:
        rt = __passage(route, sta)
    title = ' metro search '
    # res = Response(nazo(),direct_passthrough=True,mimetype='text/plain')
    return render_template("metro/list.html", subtitle=title,
                           contents=rt)

def __stations(route):
    print(route)
    rt = []
    _id = __route_table(route)
    ep = 'https://api.tokyometroapp.jp/api/v2/'
    uri = 'datapoints?rdf:type=odpt:Station&odpt:railway={}&acl:consumerKey={}'.format(_id, __key())
    url = ep + uri
    res = json.loads(rq.get(url).text)
    print(res)
    for x in [hoge['odpt:passengerSurvey'] for hoge in res]:
        for xx in x:
            rt.append([xx])
    return rt

def __passage(route, station):
    rt = []
    _id = __route_table(route)
    token = __key()
    endpoint = 'https://api.tokyometroapp.jp/api/v2/'
    uri = 'datapoints?rdf:type=odpt:Station&odpt:railway={}&acl:consumerKey={}'.format(_id, token)
    url = endpoint + uri
    res = json.loads(rq.get(url).text)
    for x in [hoge['odpt:passengerSurvey'] for hoge in res]:
        for xx in x:
            url = endpoint + "datapoints/{}?acl:consumerKey={}".format(xx, token)
            res2 = rq.get(url).text
            print(res2)
            journeys = json.loads(res2)[0]["odpt:passengerJourneys"]
            rt.append([xx, journeys])
            time.sleep(0.15)
        break
    return rt
