import requests

error = dict(message='An error Occurred', status=False)


def post(url: str, params: any, headers: any):
    try:
        request = requests.post(url, json=params, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            return error
    except:
        return error


def get(url: str, params: any, headers: any):
    try:
        request = requests.get(url, json=params, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            return error
    except:
        return error
