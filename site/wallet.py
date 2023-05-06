import bech32, random, secrets


def demo_wallet():
    """
    The function generates a Bitcoin wallet address using a randomly generated private key.
    :return: The function `demo_wallet()` returns a Bitcoin address generated from a randomly generated
    private key using the bech32 encoding scheme.
    """
    private_key = secrets.token_bytes(32)
    public_key = bech32.bech32_encode('bc', bech32.convertbits(private_key, 8, 5))
    address = bech32.bech32_encode('bc', bech32.convertbits(bech32.bech32_decode(public_key)[1], 15, 15))
    return address


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

def device_id():
    """
    The function generates a random 8-digit device ID.
    :return: The function `device_id()` returns a randomly generated string of 8 digits as the device
    ID.
    """
    dev_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return dev_id