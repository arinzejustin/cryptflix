from bitcoinaddress import Wallet
import random


def demo_wallet():
    bits = random.getrandbits(256)
    bits_hex = hex(bits)
    wallet = Wallet(bits_hex[2:])
