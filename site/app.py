from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, make_response

app = Flask(__name__)


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
        json = {'message': 'Verification Code Sent', 'saved': True}
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
        json = {'message': 'Passcode Set', 'valid': True}
        return _corsify_actual_response(jsonify(json))
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin",
                         "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, Verification, X-XSRF-TOKEN, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin",
                         "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization, Verification, X-XSRF-TOKEN, TRACK-ID")
    response.headers.add('Access-Control-Allow-Methods', "POST, GET")
    response.headers.add('Content-Type', 'application/json; charset=UTF-8')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
