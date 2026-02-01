import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
import smbprotocol

import smbclient

def get_encrypted_password_from_share(ip: str = "192.168.2.101", path: str = None) -> str:
    username = input("Please Input Samba Username: ")
    password = input("Please Input Samba Password: ")
    try:
      smbclient.ClientConfig(username=username, password=password)
      smbclient.register_session(server=ip, username=username, password=password)
    except Exception as e:
        print(e)
        exit(1)
    if path is None:
        path = fr"\\{ip}\Credentials\password.enc"
    try:
      with smbclient.open_file(path, mode="r") as fd:
          lines = fd.readlines()
    except FileNotFoundError:
        exit("Please make sure samba share is running")
    except PermissionError:
        exit("Please make sure you have permission to access the share")
    return lines[0]


def decrypt_password():
    # Read key, iv, and encrypted password from files
    with open("key_iv_file.env", "r", encoding="utf-8") as f:
        stream = f.readlines()
        key_b64 = stream[0].strip()
        iv_b64 = stream[1].strip()

    cipher_b64 = get_encrypted_password_from_share().strip()
    key = base64.b64decode(key_b64)
    iv = base64.b64decode(iv_b64)
    cipher_text = base64.b64decode(cipher_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(cipher_text) + decryptor.finalize()

    # Now remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Convert bytes back to string
    password = plaintext_bytes.decode('utf-8')
    print(password)
    return password

