
from secrets import token_bytes

KP = b'0123456789abcdef'
IV = b'fedcba9876543210'

HOST = '127.0.0.1'
KM_PORT = 5555
B_PORT = 5556


def get_random_bytes(num):
    return token_bytes(num)
