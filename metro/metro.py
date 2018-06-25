from flask import (Blueprint, Response, render_template, request)
import os, sys, time
import requests as rq
app = Blueprint('metro', __name__)


@app.route('/metro/', methods=['GET'])
def metro_mainpage():
    a = request.args.get("metro-line", "")
    nazo = [['1', '田所浩二田所田所田所田所田所田所田所田所田所田所田所田所', '3', '4']]
    title = ' metro search '
    # res = Response(nazo(),direct_passthrough=True,mimetype='text/plain')
    return render_template("metro/list.html", subtitle=title,
                           contents=nazo)

