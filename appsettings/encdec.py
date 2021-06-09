#from cryptography.fernet import Fernet
import base64
from systemid import SystemId


class EncDec:

    def __init__(self):
        self._key = SystemId().id().encode('ASCII').decode('utf-8')
        self._key_length = self._key.__len__()

    def bytes2string(self, bts):
        return bts.decode('utf-8')

    def string2bytes(self, s):
        return s.encode('utf-8')

    def encrypt(self, msg):
        key = self._key
        rkey = self._key[::-1]
        s = self.string2bytes(rkey + msg + key)
        s = base64.urlsafe_b64encode(s)
        s = self.bytes2string(s)
        return s
        # return self._fernet.encrypt(msg.encode()).decode()

    def decrypt(self, msg):
        s = base64.urlsafe_b64decode(msg)
        s = s.decode('utf-8')
        full_length = s.__len__()
        s = s[self._key_length:full_length - self._key_length]
        return s
        # msg_bytes = msg.encode()
        # return self._fernet.decrypt(msg_bytes).decode()


if __name__ == '__main__':
    ed = EncDec()
    msg = 'this is the message in clear text'
    print(msg)
    encrypted = ed.encrypt(msg)
    print(encrypted)
    decrypted = ed.decrypt(encrypted)
    print(decrypted)