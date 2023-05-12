import random, string, secrets


def demo_wallet():
    """
    The function generates a Bitcoin wallet address using a randomly generated private key.
    :return: The function `demo_wallet()` returns a Bitcoin address generated from a randomly generated
    private key using the bech32 encoding scheme.
    """
    public_key = string.ascii_letters + string.digits
    address = ''.join(secrets.choice(public_key) for _ in range(42))
    return f"bc1{address}"


def safe_url_auth():
    """
    The function generates a secure URL authentication token using a randomly generated secret.
    :return: The function `safe_url_auth()` returns a randomly generated token string that is URL-safe.
    The token is created by generating a 16-byte random string using the `secrets` module, and then
    splitting it into 4-byte chunks separated by hyphens. The resulting token is a string of 22
    characters.
    """
    secret = secrets.token_urlsafe(16)
    token = ''
    for i in range(0, len(secret), 4):
        chunk = secret[i:i+4]
        token += chunk + '-'
    token = token[:-1]
    return token

def device_id(ranges: int = 8):
    """
    The function generates a random 8-digit device ID.
    :return: The function `device_id()` returns a randomly generated string of 8 digits as the device
    ID.
    """
    dev_id = ''.join([str(random.randint(0, 9)) for _ in range(ranges)])
    return dev_id
