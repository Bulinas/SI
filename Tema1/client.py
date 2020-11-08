from Crypto.Cipher import AES

import socket
import common


if __name__ == "__main__":
    s = socket.socket()
    s.connect((common.HOST, common.KM_PORT))

    encrypted_key = s.recv(16)
    s.close()

    s = socket.socket()
    s.connect((common.HOST, common.B_PORT))

    mess = input("Enter mode(ecb/cfb): ")
    while mess != "ecb" and mess != "cfb":
        mess = input("Enter mode(ecb/cfb): ")

    s.send(encrypted_key)
    s.send(mess.encode())

    cipher = AES.new(common.KP, AES.MODE_CFB, common.IV)
    print('Encrypted key: {}'.format(encrypted_key))
    decrypted_key = cipher.decrypt(encrypted_key)
    print('Decrypted key: {}'.format(decrypted_key))

    message_flag = s.recv(16).decode()
    if message_flag != 'Start':
        print('Invalid start flag')
        exit(1)

    cipher = None
    if mess == "cfb":
        cipher = AES.new(decrypted_key, AES.MODE_CFB, iv = common.IV)
    elif mess == "ecb":
        cipher = AES.new(decrypted_key, AES.MODE_ECB)

    with open('file.txt', 'rb') as file_in:
        fl = file_in.read()
        added = 0
        while len(fl) % 16 != 0:
            added += 1
            fl += b'\0'
        encrypted = cipher.encrypt(fl)
        print(str(encrypted))
        s.send(encrypted)

        s.recv(1)
        s.send(str(added).encode())

    s.close()
