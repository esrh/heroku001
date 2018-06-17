import socket
import binascii
import json
import os
from flask import Blueprint

app = Blueprint('iwana', __name__)

@app.route('/iwana')
def iwanafunc():
    x = {}
    try:
        x["iwana_now"] = iwana_now()
    except ConnectionRefusedError:
        x["error"] = '187 refused!'
    return json.dumps(x)
    
def iwana_now():
    data = "1900d402123138377365727665722e78797a00464d4c0063dd01010009010000000006452306"
    data = binascii.unhexlify(data)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("187server.xyz" ,25565))
    client.send(data)
    response = client.recv(1024)
    ans = binascii.hexlify(response)[10:]
    ans = binascii.unhexlify(ans).decode('utf-8', 'replace') + '"}'
    ans = json.loads(ans)["players"]["online"]
    client.close()
    return ans
