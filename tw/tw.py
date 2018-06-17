# twitter


from flask import Blueprint
app = Blueprint('tw', __name__)

@app.route('/tw')
def main():
    pass


def set_keys():
    try:
        consumer = os.environ['tw_CONSUMER_KEY'],
        os.environ['tw_CONSUMER_SECRET']
    except:
        pass
    CALLBACK_URL = 'https://nazotest001.herokuapp.com/'
    app.config['twSECRET_KEY'] = os.urandom(24)
