from Crypto.Cipher import AES

import socket
import common

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((common.HOST, common.B_PORT))
        s.listen(3)

        conn, addr = s.accept()

        with conn:
            cipher = AES.new(common.KP, AES.MODE_CFB, common.IV)

            encrypted_key = conn.recv(16)
            mode = conn.recv(1024).decode()
            print('Encrypted key: {}'.format(encrypted_key))
            decrypted_key = cipher.decrypt(encrypted_key)
            print('Decrypted key: {}'.format(decrypted_key))
            print('Mode: {}'.format(mode))

            conn.send(b'Start')

            cipher = None
            if mode == "cfb":
                cipher = AES.new(decrypted_key, AES.MODE_CFB, iv = common.IV)
            elif mode == "ecb":
                cipher = AES.new(decrypted_key, AES.MODE_ECB)

            encrypted = conn.recv(1024*1024*64)
            decrypted = cipher.decrypt(encrypted)

            conn.send(b'0')
            added = int(conn.recv(1).decode())

            ln = len(decrypted)
            print(ln)

            decrypted = decrypted[:ln-added]

            print("Received:\n------------------------------")
            print(decrypted.decode('utf-8'))
