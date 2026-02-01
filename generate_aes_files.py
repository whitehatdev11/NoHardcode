from cryptography.hazmat.primitives.ciphers import Cipher, algorithms,modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import getpass
import os
import base64
def get_password() -> str:
  return getpass.getpass('Enter your password to encrypt: ')

def encrypt_password(password: str) -> bytes:
    key = os.urandom(32)# initialize our key 32*8 = 256Bit key
    iv = os.urandom(16)# Will be used to prevent frequency analysis, AKA diffusion
    cipher = Cipher(algorithms.AES(key),modes.CBC(iv),backend=default_backend())#Specifying the use of CBC mode and IV
    encryptor = cipher.encryptor() # Encrptor object for encryption
    pad128 = padding.PKCS7(128).padder() # Padding to append to key if key length isnt long enough to ensure encryption
    padded_data = (pad128.update(password.encode()) + pad128.finalize()) #Add padding to bytestring password
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    ciper_text_b64 = base64.b64encode(cipher_text).decode("utf-8") #Encode for storage
    key_b64 = base64.b64encode(key).decode("utf-8") # Encode for storage
    iv_b64 = base64.b64encode(iv).decode("utf-8")
    print("Encrypted password Base64: " + ciper_text_b64)
    print("Key Base64: " + key_b64)
    print("IV Base64: " + iv_b64)
    with open("key_iv_file.env", "w", encoding="utf-8") as f:
        f.write(key_b64 + "\n")
        f.write(iv_b64)
    with open("password.enc", "w", encoding="utf-8") as f:
        f.write(ciper_text_b64)



def main():
    password = get_password()
    encrypt_password(password)

main()


