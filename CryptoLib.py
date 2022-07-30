from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1
from Crypto.Util import Padding
import string, base64, random, os, json


class CryptoLib:
    KEY = None
    IV = None


    def get_aes_iv(self):
        return IV


    def get_aes_key(self):
        return KEY

    def init_aes(self):
        global KEY, IV
        KEY = "".join(random.choice(string.ascii_letters) for _ in range(AES.block_size))
        IV = "".join(random.choice(string.ascii_letters) for _ in range(AES.block_size))


    def set_aes(self, key:string, iv:string):
        global KEY, IV
        KEY = key
        IV = iv


    def encrypt_aes(self, data:string)->string:
        aes_cipher = AES.new(KEY.encode(), AES.MODE_CBC, IV.encode())
        data = Padding.pad(data.encode(), AES.block_size, 'pkcs7')
        encrypted_data = aes_cipher.encrypt(data)
        return base64.b64encode(encrypted_data)


    def decrypt_aes(self, data:string)->string:
        aes_cipher = AES.new(KEY.encode(), AES.MODE_CBC, IV.encode())
        encrypted_data = base64.b64decode(data)
        decrypted_data = aes_cipher.decrypt(encrypted_data)
        return Padding.unpad(decrypted_data, AES.block_size, 'pkcs7').decode()


    def init_rsa(self):
        if not os.path.exists("public.pem"):
            keygen = RSA.generate(2048)
            with open("private.pem", "wb") as f:
                f.write(keygen.export_key())
            with open("public.pem", "wb") as f:
                f.write(keygen.publickey().export_key())


    def encrypt_rsa(self, data:string)->string:
        with open("public.pem", "r") as f:
            pubkey = RSA.importKey(f.read())
        rsa_cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA1)
        return base64.b64encode(rsa_cipher.encrypt(data.encode()))


    def decrypt_rsa(self, data:string)->string:
        with open("private.pem", "r") as f:
            privkey = RSA.importKey(f.read())
        rsa_cipher = PKCS1_OAEP.new(privkey, hashAlgo=SHA1)
        return rsa_cipher.decrypt(base64.b64decode(data)).decode()
