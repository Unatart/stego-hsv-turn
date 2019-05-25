import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


class AESError(Exception):
    pass


class AESCipher(object):
    def __init__(self):
        self.__key__ = hashlib.sha256(b'16-character key').digest()

    def encrypt(self, raw):
        try:
            BS = AES.block_size
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

            raw = base64.b64encode(pad(raw).encode('utf8'))
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key=self.__key__, mode=AES.MODE_CFB, iv=iv)
        except:
            raise AESError('not valid raw')

        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        try:
            unpad = lambda s: s[:-ord(s[-1:])]

            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.__key__, AES.MODE_CFB, iv)
        except:
            raise AESError('not valid enc')

        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))
