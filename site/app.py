import hashlib
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from jwt_token import authorize

from query import add, db_admin__, db_admin_add, db_history, db_login, db_password__, db_profile__, db_ref, db_trans, db_update, db_users__, db_verify, db_passcode, db_onboard, db_safe_, fetch_user, update_user_balance
from netrequest import get
from wallet import safe_url_auth

app = Flask(__name__)
load_dotenv()
now = datetime.now()
curr_time = now.strftime("%B %d, %Y %H:%M:%S")
created = f"{now.strftime('%B %d, %Y')} at {now.strftime('%H:%M:%S')}"
admin_req = f"{now.strftime('%B %d, %Y')}"

ALLOWED_HOST = os.getenv('ALLOWED_HOST')
AVI_URL = os.getenv('AVI_URL')
NEWS_KEY = os.getenv('NEWS_KEY')
HOST = os.getenv('NEWS_HOST')
cookie_domain = os.getenv('COOKIE_DOMAIN')


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
        country = data['country']
        reg = db_onboard(email=email, name=name, tel=tel,
                         country=country, time=created)
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
        if len(password) < 8:
            return _corsify_actual_response(jsonify({'message': 'Passcode is too short', 'status': False}))
        insert = db_passcode(uid=uuid, passcode=confirm)
        response = make_response(jsonify(insert))
        response = _corsify_actual_response(response)
        if insert['status']:
            # set cookies
            response.set_cookie(key='uuid', value=insert['uuid'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='user', value=insert['email'], max_age=3600, expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='token', value=insert['bearer'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='card', value=insert['role'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='ssid', value=insert['ssid'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
        return response
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/login', methods=['POST', 'OPTIONS'])
def login():
    response = make_response()
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        data = request.get_json(force=True)
        email = data['email']
        passcode = data['pass']
        if not email or not passcode:
            return _corsify_actual_response(jsonify({'message': 'Invalid Credentials', 'status': False}))
        login_query = db_login(email=email, password=passcode)
        response = make_response(jsonify(login_query))
        response = _corsify_actual_response(response)
        if login_query['status']:
            # set cookies
            response.set_cookie(key='uuid', value=login_query['uuid'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='user', value=login_query['email'], max_age=3600, expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='token', value=login_query['bearer'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='card', value=login_query['role'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
            response.set_cookie(key='ssid', value=login_query['ssid'], expires=datetime.now(
            ) + timedelta(days=30), path='/', domain=cookie_domain, secure=True, httponly=True, samesite='lax')
        return response
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
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        cookies = dict(uuid=uuid,
                       ssid=request.cookies.get('ssid'))
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = db_trans(uuid=uuid)
        return _corsify_actual_response(jsonify(data))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/magic_auth', methods=['POST', 'OPTIONS'])
def magic_auth():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        cookies = dict(uuid=request.cookies.get('uuid'),
                       ssid=request.cookies.get('ssid'))
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        uuid = request.cookies.get('uuid')
        token = safe_url_auth()
        res = db_safe_(magic=token, uuid=uuid)
        return _corsify_actual_response(jsonify(res))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/password__', methods=['POST', 'OPTIONS'])
def password__():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        cookies = dict(uuid=request.cookies.get('uuid'),
                       ssid=request.cookies.get('ssid'))
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        uuid = request.cookies.get('uuid')
        data = request.get_json(force=True)
        update = data['update']
        res = db_password__(
            uuid=uuid, passcode=data['passcode'], update=update)
        return _corsify_actual_response(jsonify(res))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/news', methods=['POST', 'OPTIONS'])
def news():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        query = data['query']
        from_ = data['from']
        to = data['to']
        res = get(url=f'{HOST}/news', params=dict(apiKey=NEWS_KEY,
                  q=query, from_date=from_, to_date=to))
        return _corsify_actual_response(jsonify(res))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', type='404', description=error)


@app.route('/api/bob/user', methods=['POST', 'OPTIONS'])
def user():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.headers.get('uuid')
        ssid = request.headers.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        user = fetch_user(uuid=uuid)
        user.update({'last': curr_time})
        return _corsify_actual_response(jsonify(user))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/add_trans', methods=['POST', 'OPTIONS'])
def add_trans():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        authorization = request.headers.get('authorization')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=request.cookies.get('uuid'),
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        uuid = request.cookies.get('uuid')
        adds = add(amount=str(data['amount']), type_=data['type'], time=curr_time, uuid=uuid,
                   status='pending', coin=data['coin'], address=data['address'], session=ssid)
        return _corsify_actual_response(jsonify(adds))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/user_details', methods=['POST', 'OPTIONS'])
def user_details():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.cookies.get('token')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, data={'authenticate': False, 'message': 'Invalid user keys'})))
        user = dict(status=True, data=dict(
            authorization=authorization, ssid=ssid, authenticate=True))
        return _corsify_actual_response(jsonify(user))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/ref', methods=['POST', 'OPTIONS'])
def ref():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = request.get_json(force=True)
        refer = db_ref(user=data['user'])
        return _corsify_actual_response(jsonify(refer))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/admin__', methods=['POST', 'OPTIONS'])
def admin__():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.headers.get('uuid')
        ssid = request.headers.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        admin = db_admin__(date=admin_req)
        return _corsify_actual_response(jsonify(admin))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/users__', methods=['POST', 'OPTIONS'])
def users__():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        users = db_users__()
        return _corsify_actual_response(jsonify(users))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/user/profile', methods=['POST', 'OPTIONS'])
def profile__():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.headers.get('uuid')
        ssid = request.headers.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = request.get_json(force=True)
        uid = data['uuid']
        users = db_profile__(uuid=uid)
        return _corsify_actual_response(jsonify(users))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/admin/update', methods=['POST', 'OPTIONS'])
def update():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = request.get_json(force=True)
        uid = data['id']
        status = data['status']
        deposit = data['deposit']
        balance = data['balance']
        plan = data['plan']
        update = db_update(uid=uid, plan=plan, balance=balance,
                           deposit=deposit, status=status)
        return _corsify_actual_response(jsonify(update))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/admin/history__', methods=['POST', 'OPTIONS'])
def history__():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = request.get_json(force=True)
        uid = data['uid']
        history = db_history(uid=uid)
        return _corsify_actual_response(jsonify(history))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/transaction/update', methods=['POST', 'OPTIONS'])
def trans_update():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = request.get_json(force=True)
        uid = data['uid']
        ids = data['id']
        transaction_type = data['type']
        status = data['status']
        amount = data['amount']
        update__ = update_user_balance(value=amount, uid=uid, ids=ids, status=status, transaction_type=transaction_type)
        return _corsify_actual_response(jsonify(update__))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route('/api/bob/admin/add', methods=['POST', 'OPTIONS'])
def admin_add():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    if request.method == "POST":
        authorization = request.headers.get('authorization')
        uuid = request.cookies.get('uuid')
        ssid = request.cookies.get('ssid')
        cookies = dict(uuid=uuid,
                       ssid=ssid)
        auth = authorize(cookie=cookies, token=authorization)
        if not auth:
            return _corsify_actual_response(jsonify(dict(status=False, message='Failed verification')))
        data = request.get_json(force=True)
        name = data['name']
        deposit = data['deposit']
        balance = data['balance']
        passcode = data['passcode']
        country = data['country']
        email = data['email']
        tel = data['tel']
        plan = data['plan']
        add__ = db_admin_add(email=email, name=name, passcode=passcode, deposit=deposit, balance=balance, plan=plan, tel=tel, created=created, country=country)
        return _corsify_actual_response(jsonify(add__))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))
        

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
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization")
    response.headers.add('Access-Control-Allow-Methods', "OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


def _corsify_actual_response(response):
    """
    It adds the following headers to the response:

    Access-Control-Allow-Origin: ALLOWED_HOST
    Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization,
    Verification
    Access-Control-Allow-Methods: POST, GET
    Content-Type: application/json; charset=UTF-8
    Access-Control-Allow-Credentials: true

    """
    response.headers.add("Access-Control-Allow-Origin",
                         ALLOWED_HOST)
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, Authorization")
    response.headers.add('Access-Control-Allow-Methods', "POST")
    response.headers.add('Content-Type', 'application/json; charset=UTF-8')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
