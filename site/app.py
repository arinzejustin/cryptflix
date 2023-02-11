import os, hashlib, uuid
from flask import Flask, render_template, Response, request, jsonify, redirect, send_from_directory, make_response
from dotenv import load_dotenv
from jwt_token import authenticate, generate, authorize
from query import db_login
from netrequest import post

app = Flask(__name__)
load_dotenv()

ALLOWED_HOST = os.getenv('ALLOWED_HOST')
ENV_AVI_URL = os.getenv('ENV_AVI_URL')


@app.route('/index')
@app.route('/')
@app.route('/home')
def index():
    return send_from_directory('.svelte-kit/output/prerendered/pages', 'index.html')


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
        star = email[:2]
        domain = email.split('@')[1]
        json = {'message': f'Verification Code Sent to {star}*****@{domain}', 'saved': True}
        return _corsify_actual_response(jsonify(json))
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
        uuid = data['uuid']
        json = {'message': 'Authorization Successful', 'valid': True}
        return _corsify_actual_response(jsonify(json))
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
            return _corsify_actual_response(jsonify({'message': 'Passcode does not match', 'saved': False}))
        return _corsify_actual_response(jsonify({'message': '', 'saved': True}))
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
        json = {'gravatar': f'{ENV_AVI_URL}/{result}?d=robohash&f=y&s=50', 'email': user}
        print(json)
        return _corsify_actual_response(jsonify(json))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', type='404', description=error)


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
