from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, make_response

app = Flask(__name__)


@app.route('/index')
@app.route('/')
@app.route('/home')
def index():
    return send_from_directory('.svelte-kit/output/prerendered/pages', 'index.html')

@app.route('/about')
def about():
    return jsonify({'hello': 'world'})


@app.route("/<path:path>")
def home(path):
    return send_from_directory('.svelte-kit/output/client', path)


@app.route('/api/bob/login')
def login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        return _corsify_actual_response(jsonify({"login": True}))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=3000, debug=True)
