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
    return None

def __station_table(route, station):
    df = pd.read_csv('metro/station_table.csv')
    for i, row in df.iterrows():
        if row['route'] == route and row['station'] == station:
            return row['id']
    return None

@app.route('/metro/', methods=['GET'])
def metro_mainpage():
    return render_template("metro/base.html")

@app.route('/metro/passengers/', methods=['GET'])
def metro_passengers():
    route = request.args.get("metro-line", '')
    sta = request.args.get("metro-station", '')
    if route == '' and sta == '':
        rt = ''
    elif sta == '':
        rt = __stations(route)
    elif route == '':
        rt = ''
    else:
        rt = __passage(route, sta)
    title = ' metro passengers search '
    # res = Response(nazo(),direct_passthrough=True,mimetype='text/plain')
    return render_template("metro/list.html", subtitle=title,
                           contents=rt)

def __stations(route):
    print(route)
    rt = []
    _id = __route_table(route)
    if _id:
        ep = 'https://api.tokyometroapp.jp/api/v2/'
        uri = 'datapoints?rdf:type=odpt:Station&odpt:railway={}&acl:consumerKey={}'.format(_id, __key())
        url = ep + uri
        res = json.loads(rq.get(url).text)
        print(res)
        for hoge in res:
            rt.append([hoge['odpt:passengerSurvey'][0].rsplit(".", 1)[0], hoge['dc:title']])
    return rt

def __passage(route, station):
    rt = []
    # step1
    _id = __route_table(route)
    if _id:
        token = __key()
        endpoint = 'https://api.tokyometroapp.jp/api/v2/'
        uri = 'datapoints?rdf:type=odpt:Station&odpt:railway={}&acl:consumerKey={}'.format(_id, token)
        url = endpoint + uri
        res = json.loads(rq.get(url).text)
        # step2
        _id = __station_table(route, station)
        if _id:
            for x in res:
                if x['owl:sameAs'] == _id:
                    for xx in x['odpt:passengerSurvey']:
                        url = endpoint + "datapoints/{}?acl:consumerKey={}".format(xx, token)
                        res2 = rq.get(url).text
                        # print(res2)
                        journeys = json.loads(res2)[0]["odpt:passengerJourneys"]
                        rt.append([xx, journeys])
                        time.sleep(0.15)
    return rt
