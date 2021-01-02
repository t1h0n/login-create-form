import os
import xxtea
import binascii
from getmac import get_mac_address as gma


key = gma().replace(':', '', 1).encode('utf-8')
sep = os.linesep.encode('utf-8')
dataFile = 'data/hashed_data.b'


def memorizeAccount(login, password):
    enc_login = xxtea.encrypt_hex(
        login.encode('utf-8'), key)
    enc_password = xxtea.encrypt_hex(
        password.encode('utf-8'),  key)
    with open(dataFile, 'wb') as f:
        f.write(enc_login+sep +
                enc_password+sep)


def storedDataExists():
    return os.path.exists(dataFile)

def removeDataFile():
    os.remove(dataFile)

def loadMemorizedAccount():
    with open(dataFile, 'rb') as f:
        enc_login = f.readline().rstrip(sep)
        enc_password = f.readline().rstrip(sep)
    login = xxtea.decrypt_hex(enc_login,  key)
    password = xxtea.decrypt_hex(enc_password,  key)
    return login.decode('utf-8'), password.decode('utf-8')
