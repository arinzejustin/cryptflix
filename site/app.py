import hashlib
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response

from query import db_login, db_verify, db_passcode, db_onboard, db_safe_
from netrequest import get
from wallet import safe_url_auth

app = Flask(__name__)
load_dotenv()
now = datetime.now()
curr_time = now.strftime("%B %d, %Y %H:%M:%S")

ALLOWED_HOST = os.getenv('ALLOWED_HOST')
AVI_URL = os.getenv('AVI_URL')
NEWS_KEY = os.getenv('NEWS_KEY')
HOST = os.getenv('NEWS_HOST')


@app.route('/index')
@app.route('/')
@app.route('/index/')
def index():
    return send_from_directory('.svelte-kit/output/prerendered/pages', 'index.html')


@app.route('/about')
@app.route('/about/')
def about():
    return send_from_directory('.svelte-kit/output/prerendered/pages', 'about.html')

@app.route('/news')
def news_():
    return send_from_directory('templates', 'news.json')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('.svelte-kit/output/client', path)


@app.route('/api/bob/onboard', methods=['POST', 'OPTIONS'])
def onboard():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json(force=True)
        email = data['email']
        name = data['name']
        tel = data['tel']
        reg = db_onboard(email=email, name=name, tel=tel)
        return _corsify_actual_response(jsonify(reg))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/verify', methods=['POST', 'OPTIONS'])
def verify():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json(force=True)
        code = data['verify']
        email = data['email']
        response = db_verify(email=email, code=code, insert=False)
        return _corsify_actual_response(jsonify(response))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/password', methods=['POST', 'OPTIONS'])
def passcode():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json(force=True)
        password = data['passcode']
        confirm = data['confirm']
        uuid = data['uuid']
        if password != confirm:
            return _corsify_actual_response(jsonify({'message': 'Passcode does not match', 'status': False}))
        insert = db_passcode(uuid=uuid, passcode=confirm)
        return _corsify_actual_response(jsonify(insert))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json(force=True)
        email = data['email']
        passcode = data['pass']
        if not email or not passcode:
            return _corsify_actual_response(jsonify({'message': 'Invalid Credentials', 'status': False}))
        login_query = db_login(email=email, password=passcode)
        return _corsify_actual_response(jsonify(login_query))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/gravatar', methods=['GET'])
def gravatar():
    if request.method == "GET":
        data = request.get_json(force=True)
        user = data['user']
        result = hashlib.md5(user.lower().encode()).hexdigest()
        avi = {'gravatar': f'{AVI_URL}/{result}?d=robohash&f=y&s=50'}
        return _corsify_actual_response(jsonify(avi))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/market', methods=['POST', 'OPTIONS'])
def market():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        path = data['path']
        query = dict(query=data['query'])
        res = get(url=f'https://markets.api.bitcoin.com/{path}')
        res.update(query)
        return _corsify_actual_response(jsonify(res))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/transactions', methods=['POST', 'OPTIONS'])
def transactions():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        res = dict(data=[{
            'type_': 'Withdraw',
            'status': 'failed',
            'time': curr_time,
            'amount': '-$2,000'
        },
            {
            'type_': 'Deposit',
            'status': 'success',
            'time': curr_time,
            'amount': '$1,000'
        },
            {
            'type_': 'Deposit',
            'status': 'pending',
            'time': curr_time,
            'amount': '$4,000'
        }])
        return _corsify_actual_response(jsonify(res))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/magic_auth', methods=['POST', 'OPTIONS'])
def magic_auth():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        token = safe_url_auth()
        res = db_safe_(magic=token, uuid='')
        return _corsify_actual_response(jsonify(res))


@app.route('/api/bob/news', methods=['POST', 'OPTIONS'])
def news():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        query = data['query']
        from_ = data['from']
        to = data['to']
        res = get(url = f'{HOST}/news', params = dict(apiKey=NEWS_KEY,q=query, from_date=from_, to_date=to))
        return _corsify_actual_response(jsonify(res))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', type='404', description=error)

def cookie():
    return

def _build_cors_preflight_response():
    """
    It returns a response object with the appropriate headers to allow CORS requests from the specified
    domain
    :return: A response object with the headers set to allow CORS.
    """
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin",
                         ALLOWED_HOST)
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def _corsify_actual_response(response):
    """
    It adds the following headers to the response:

    Access-Control-Allow-Origin: ALLOWED_HOST
    Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization,
    Verification, TRACK-ID
    Access-Control-Allow-Methods: POST, GET
    Content-Type: application/json; charset=UTF-8
    Access-Control-Allow-Credentials: true

    """
    response.headers.add("Access-Control-Allow-Origin",
                         ALLOWED_HOST)
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "POST")
    response.headers.add('Content-Type', 'application/json; charset=UTF-8')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
