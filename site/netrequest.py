import requests

error = dict(message='An error Occurred', status=False)


def post(url: str, params: any, headers: any = ''):
    """
    It takes a url, params, and headers as arguments, and returns a response object
    
    :param url: The URL of the API endpoint
    :type url: str
    :param params: any = {'key': 'value'}
    :type params: any
    :param headers: {'Content-Type': 'application/json'}
    :type headers: any
    :return: A dictionary with the key 'status' and the value True.
    """
    try:
        request = requests.post(url, json=params, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            return error
    except:
        return error


def get(url: str, params: any ='', headers: any =''):
    """
    It takes a url, params, and headers as arguments, and returns a response object
    
    :param url: str = 'https://api.cryptflixinvest.com/users/{}/history'.format(username)
    :type url: str
    :param params: {'param1': 'value1', 'param2': 'value2'}
    :type params: any
    :param headers: {'Authorization': 'Bearer ' + token}
    :type headers: any
    :return: None
    """
    try:
        request = requests.get(url, json=params, headers=headers)
        if request.status_code == 200:
            response = request.json()
            response.update({'status': True})
            return response
        else:
            return error
    except:
        return error
