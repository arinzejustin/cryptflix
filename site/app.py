import os, hashlib, uuid
from flask import Flask, render_template, Response, request, jsonify, redirect, send_from_directory, make_response
from dotenv import load_dotenv
from jwt_token import auth, generate
from werkzeug.security import generate_password_hash, check_password_hash

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
        print(confirm, password)
        if password == confirm:
            return _corsify_actual_response(jsonify({'message': 'Passcode does not match', 'error': True}))
        hashs = generate_password_hash(confirm, "pbkdf2:SHA256", 100)
        return _corsify_actual_response(jsonify({'message': '', 'saved': True, 'passcode': hashs}))
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
        json = {'email': email, 'pass': passcode}
        return _corsify_actual_response(jsonify(json))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/gravatar', methods=['GET'])
def gravatar():
    if request.method == "GET":
        data = request.get_json(force=True)
        email = data['email']
        result = hashlib.md5(email.lower().encode()).hexdigest()
        json = {'gravatar': f'{ENV_AVI_URL}/{result}?d=robohash&f=y&s=100'}
        return _corsify_actual_response(jsonify(json))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')


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
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRF-TOKEN, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def _corsify_actual_response(response):
    """
    It adds the following headers to the response:
    
    Access-Control-Allow-Origin: ALLOWED_HOST
    Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization,
    Verification, X-CSRF-TOKEN, TRACK-ID
    Access-Control-Allow-Methods: POST, GET
    Content-Type: application/json; charset=UTF-8
    Access-Control-Allow-Credentials: true
    
    """
    response.headers.add("Access-Control-Allow-Origin",
                         ALLOWED_HOST)
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRF-TOKEN, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "POST")
    response.headers.add('Content-Type', 'application/json; charset=UTF-8')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
