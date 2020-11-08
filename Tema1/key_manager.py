# https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/#2_Generating_a_Key
# https://realpython.com/python-sockets/

from Crypto.Cipher import AES

import common
import socket


class KeyManager():

    def __init__(self):
        self.kp = common.KP
        self.iv = common.IV

    def get_k(self):
        cipher = AES.new(self.kp, AES.MODE_CFB, self.iv)
        raw_key = common.get_random_bytes(16)
        print('Generated key: {}'.format(raw_key))
        encrypted_key = cipher.encrypt(raw_key)
        print('Encrypted key: {}'.format(encrypted_key))
        return encrypted_key

    def start(self):
        print('Kp: {}'.format(self.kp))
        print('Iv: {}'.format(self.iv))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((common.HOST, common.KM_PORT))
            s.listen(3)

            while True:
                conn, addr = s.accept()
                with conn:
                    print('{} connected!'.format(addr))
                    conn.send(self.get_k())


if __name__ == "__main__":
    km = KeyManager()
    km.start()
