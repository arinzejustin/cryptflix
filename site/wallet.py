from bitcoinaddress import Wallet
import random
import secrets


def demo_wallet():
    """
    It generates a random 256 bit number, converts it to hexadecimal, and then uses the first 64
    characters of the hexadecimal number to create a wallet
    """
    bits = random.getrandbits(256)
    bits_hex = hex(bits)
    wallet = Wallet(bits_hex[2:])
    return wallet


def safe_url_auth():
    secret = secrets.token_urlsafe(16)
    token = ''
    for i in range(0, len(secret), 4):
        chunk = secret[i:i+4]
        token += chunk + '-'
    token = token[:-1]
    return token
