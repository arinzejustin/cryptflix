from bitcoinaddress import Wallet
import random


def demo_wallet():
    """
    It generates a random 256 bit number, converts it to hexadecimal, and then uses the first 64
    characters of the hexadecimal number to create a wallet
    """
    bits = random.getrandbits(256)
    bits_hex = hex(bits)
    wallet = Wallet(bits_hex[2:])

x = {1: 'a', 2: 'b'}
y = x.keys()
print(y)